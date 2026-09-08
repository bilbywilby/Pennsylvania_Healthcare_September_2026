import { useState, useEffect, useCallback, useRef } from 'react';

export interface OutboxOperation {
  opType: string;
  payload: unknown;
}

export type OutboxItemStatus = 'pending' | 'deferred' | 'processing' | 'failed';

export interface OutboxItem {
  id: string; // Stable idempotency key (UUID v4)
  op: OutboxOperation;
  createdAt: number;
  retryCount: number;
  nextAttemptAt: number;
  status: OutboxItemStatus;
  lastError?: string;
}

export interface DispatchClientEnv {
  apiBase: string;
  hmacSecret: string;
}

const DEFAULT_RETRY_AFTER_MS = 5000;
const MAX_RETRIES = 5;

/**
 * Parses the HTTP `Retry-After` header value which can be either:
 * - Delay in seconds (e.g., "5")
 * - An HTTP-date string (e.g., "Wed, 21 Oct 2026 07:28:00 GMT")
 */
function parseRetryAfterHeader(headerValue: string | null): number {
  if (!headerValue) return DEFAULT_RETRY_AFTER_MS;

  const seconds = parseInt(headerValue, 10);
  if (!isNaN(seconds)) {
    return Math.max(1, seconds) * 1000;
  }

  const dateMs = Date.parse(headerValue);
  if (!isNaN(dateMs)) {
    const diff = dateMs - Date.now();
    return diff > 0 ? diff : DEFAULT_RETRY_AFTER_MS;
  }

  return DEFAULT_RETRY_AFTER_MS;
}

/**
 * Calculates exponential backoff with full jitter for general retryable errors.
 */
function calculateBackoffMs(retryCount: number): number {
  const baseMs = 1000;
  const maxMs = 30000;
  const temp = Math.min(maxMs, baseMs * Math.pow(2, retryCount));
  return Math.floor(Math.random() * temp);
}

/**
 * Sends a canonical signed POST request to the Worker API.
 */
export async function signedDispatch(
  env: DispatchClientEnv,
  op: OutboxOperation,
  idempotencyKey: string,
): Promise<Response> {
  const bodyText = JSON.stringify(op);
  const timestamp = Date.now().toString(); // Epoch milliseconds
  const url = new URL(`${env.apiBase}/api/sync`);

  const canonicalPayload = `POST ${url.pathname}\n${timestamp}\n${bodyText}`;

  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(env.hmacSecret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign'],
  );

  const sig = await crypto.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode(canonicalPayload),
  );

  const hex = Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  return fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Idempotency-Key': idempotencyKey,
      'X-Timestamp': timestamp,
      'X-Signature-256': `sha256=${hex}`,
    },
    body: bodyText,
  });
}

/**
 * Custom hook to manage outbox operations, signing, and background delivery loops.
 */
export function useOutboxSync(env: DispatchClientEnv) {
  const [queue, setQueue] = useState<OutboxItem[]>([]);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const isProcessingRef = useRef<boolean>(false);

  // Enqueue a new operation. Mint a stable idempotency key immediately.
  const enqueue = useCallback((opType: string, payload: unknown): string => {
    const id = crypto.randomUUID();
    const newItem: OutboxItem = {
      id,
      op: { opType, payload },
      createdAt: Date.now(),
      retryCount: 0,
      nextAttemptAt: Date.now(),
      status: 'pending',
    };

    setQueue((prev) => [...prev, newItem]);
    return id;
  }, []);

  // Process the queue item by item sequentially.
  const processQueue = useCallback(async () => {
    if (isProcessingRef.current) return;
    isProcessingRef.current = true;
    setIsSyncing(true);

    try {
      let candidate = queue.find(
        (item) =>
          (item.status === 'pending' || item.status === 'deferred') &&
          Date.now() >= item.nextAttemptAt,
      );

      while (candidate) {
        const itemId = candidate.id;

        // Mark as in-flight
        setQueue((prev) =>
          prev.map((it) =>
            it.id === itemId ? { ...it, status: 'processing' } : it,
          ),
        );

        let response: Response | null = null;
        let networkError: Error | null = null;

        try {
          response = await signedDispatch(env, candidate.op, candidate.id);
        } catch (err) {
          networkError = err instanceof Error ? err : new Error(String(err));
        }

        if (response && (response.status === 200 || response.status === 202)) {
          // Success: remove item from outbox queue
          setQueue((prev) => prev.filter((it) => it.id !== itemId));
        } else if (response && response.status === 409) {
          // Concurrency lock detected (another tab or request currently processing)
          const retryAfterMs = parseRetryAfterHeader(
            response.headers.get('Retry-After'),
          );

          setQueue((prev) =>
            prev.map((it) => {
              if (it.id !== itemId) return it;
              return {
                ...it,
                status: 'deferred',
                nextAttemptAt: Date.now() + retryAfterMs,
                // CRITICAL: retryCount is intentionally NOT incremented for 409
              };
            }),
          );
        } else {
          // Transient failure (5xx, network error, or rate limits)
          const isFatal = response && response.status >= 400 && response.status < 500;

          setQueue((prev) =>
            prev.map((it) => {
              if (it.id !== itemId) return it;
              const newRetryCount = it.retryCount + 1;
              const hasExceededRetries = newRetryCount >= MAX_RETRIES;

              if (isFatal || hasExceededRetries) {
                return {
                  ...it,
                  status: 'failed',
                  retryCount: newRetryCount,
                  lastError: networkError
                    ? networkError.message
                    : `HTTP ${response?.status}`,
                };
              }

              return {
                ...it,
                status: 'pending',
                retryCount: newRetryCount,
                nextAttemptAt: Date.now() + calculateBackoffMs(newRetryCount),
                lastError: networkError
                  ? networkError.message
                  : `HTTP ${response?.status}`,
              };
            }),
          );
        }

        // Find next processable item
        const now = Date.now();
        candidate = queue.find(
          (item) =>
            item.id !== itemId &&
            (item.status === 'pending' || item.status === 'deferred') &&
            now >= item.nextAttemptAt,
        );
      }
    } finally {
      isProcessingRef.current = false;
      setIsSyncing(false);
    }
  }, [env, queue]);

  // Periodic poll timer to re-trigger queue processing when deferred items mature
  useEffect(() => {
    const timer = setInterval(() => {
      const hasReadyItems = queue.some(
        (item) =>
          (item.status === 'pending' || item.status === 'deferred') &&
          Date.now() >= item.nextAttemptAt,
      );
      if (hasReadyItems) {
        processQueue();
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [queue, processQueue]);

  const retryFailed = useCallback((id?: string) => {
    setQueue((prev) =>
      prev.map((it) => {
        if (id && it.id !== id) return it;
        if (it.status === 'failed') {
          return {
            ...it,
            status: 'pending',
            retryCount: 0,
            nextAttemptAt: Date.now(),
          };
        }
        return it;
      }),
    );
  }, []);

  return {
    enqueue,
    queue,
    isSyncing,
    retryFailed,
  };
}
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "=== Starting Audit Bootstrap Sequence ==="
echo "Root: $PROJECT_ROOT"

run_and_validate() {
    local script="$1"
    local desc="$2"

    echo ">>> Running: $desc"
    if python3 "$script"; then
        echo "[OK] $desc completed successfully."
    else
        echo "[FAIL] $desc failed. Stopping bootstrap."
        exit 1
    fi
}

found_any=0
for script in "$SCRIPT_DIR"/[0-9][0-9]_*.py; do
    if [[ -f "$script" ]]; then
        found_any=1
        run_and_validate "$script" "$(basename "$script")"
    fi
done

if [[ "$found_any" -eq 0 ]]; then
    echo "WARNING: No bootstrap scripts found in $SCRIPT_DIR"
    exit 1
fi

echo "=== Bootstrap Sequence Complete ==="

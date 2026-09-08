#!/usr/bin/env python3
"""
04_audit.py - Carrier Rate Filing Auditor (pre-flight validation gate)

Validates data/public/approved_rates_2026.csv (carrier-level PID rate
filings) structurally and against the crosswalk's known rating areas,
before 05_ingest_carrier_extensions.py performs full ingestion and
aggregation on the same file.

REPURPOSED: an earlier draft of this script modeled a per-county/age/
plan_type consumer premium file. That dataset was never actually produced
anywhere in this pipeline (no generator wrote it, nothing else consumed
it, and the full test suite passed without it) — the real artifact your
PID filings produce is this carrier-level rate-change file. See
data/README.md for the retirement note and the reserved filename for a
future genuine consumer-level extract; CMS's State-Based Exchange QHP
Public Use Files (which do cover Pennsylvania/Pennie) are the realistic
source if that's ever built — verify the exact PUF file's schema against
your needs before relying on it, this hasn't been done here.

Intentionally a fast, read-only pass/fail check with no side effects (no
anomaly CSV, no aggregation) — 05_ingest_carrier_extensions.py already
does that heavier work on the same input. Run this as a cheap pre-commit
or CI gate ahead of it.

No hardcoded carrier-name allowlist: PID's actual 2026 individual-market
filings include e.g. three separate UPMC entities and five separate
Highmark entities, each with its own rate and rating areas, and that
roster changes every filing cycle. A fixed list goes stale by definition;
this validates structure (non-empty carrier name, parseable rate within
sane bounds, valid rating area(s)) instead.
"""
import csv
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path("data")
CARRIER_RATES_FILE = DATA_DIR / "public" / "approved_rates_2026.csv"
CROSSWALK_FILE = DATA_DIR / "public" / "pa_county_fips_crosswalk.json"

REQUIRED_BASE_COLS = ["carrier_name", "approved_rate_change"]
AREA_COLS = ("rating_area", "primary_rating_areas")

# Sanity bounds to catch data-entry errors (a stray digit, a misplaced
# decimal), NOT a verified statutory cap — no such cap was confirmed during
# research for this script. Widen if a real filing legitimately exceeds
# this (2026's highest approved individual-market rate was 37.8%).
MIN_SANE_RATE_CHANGE = Decimal("-75.00")
MAX_SANE_RATE_CHANGE = Decimal("100.00")


class AuditError(Exception):
    """Base exception for audit operations."""


class AuditSchemaError(AuditError):
    """Raised when the file/crosswalk is missing, unreadable, or missing
    required columns. Individual bad rows are collected as findings, not
    raised as exceptions — see audit_carrier_rates()."""


def load_crosswalk() -> Dict[str, Dict[str, str]]:
    """Loads crosswalk JSON into a case-insensitive lookup keyed by lowercase
    county name. Accepts either crosswalk shape currently in circulation:
      - area-keyed:  {"1": [{"county": "...", "fips": "..."}], "2": [...], ...}
      - flat-list:   {"state_fips": "42", "state_abbr": "PA",
                      "counties": [{"fips": "...", "canonical_name": "...", "rating_area": 1}, ...]}
    """
    if not CROSSWALK_FILE.exists():
        raise AuditSchemaError(f"Crosswalk file not found: {CROSSWALK_FILE}")

    with open(CROSSWALK_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise AuditSchemaError(f"Crosswalk file is not valid JSON: {e}") from e

    county_map = {}
    try:
        if isinstance(data, dict) and "counties" in data:
            for item in data["counties"]:
                key = str(item["canonical_name"]).strip().lower()
                county_map[key] = {
                    "display_name": str(item["canonical_name"]).strip(),
                    "fips": str(item["fips"]),
                    "area": str(item["rating_area"]),
                }
        else:
            for area_id, counties in data.items():
                for item in counties:
                    key = str(item["county"]).strip().lower()
                    county_map[key] = {
                        "display_name": str(item["county"]).strip(),
                        "fips": str(item["fips"]),
                        "area": str(area_id),
                    }
    except (TypeError, KeyError) as e:
        raise AuditSchemaError(f"Crosswalk file has an unrecognized structure: {e}") from e

    if not county_map:
        raise AuditSchemaError("Crosswalk loaded but contains no counties.")

    return county_map


def parse_rating_areas(raw: str) -> List[str]:
    """Parses a rating-area field into a de-duplicated, order-preserving list
    of area-id strings. Supports a bare id ("8"), a dash range ("1-9"), a
    semicolon-separated list ("6;7;9"), and combinations ("1-3;7")."""
    areas: List[str] = []
    for token in raw.split(";"):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start_str, _, end_str = token.partition("-")
            start, end = int(start_str.strip()), int(end_str.strip())
            if end < start:
                raise ValueError(f"range end before start: '{token}'")
            areas.extend(str(a) for a in range(start, end + 1))
        else:
            areas.append(str(int(token)))

    seen = set()
    deduped = []
    for a in areas:
        if a not in seen:
            seen.add(a)
            deduped.append(a)
    return deduped


def audit_carrier_rates() -> Dict:
    """Runs structural + crosswalk validation over CARRIER_RATES_FILE.
    Never calls sys.exit — safe to import and call. Raises AuditSchemaError
    only for file-level problems (missing file, missing headers); individual
    bad rows are returned as findings in the result dict."""
    if not CARRIER_RATES_FILE.exists():
        raise AuditSchemaError(f"Carrier rates file not found: {CARRIER_RATES_FILE}")

    county_map = load_crosswalk()
    valid_areas = {info["area"] for info in county_map.values()}

    findings = []
    total = 0
    valid = 0

    with open(CARRIER_RATES_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise AuditSchemaError("Carrier rates CSV is empty or missing headers.")

        headers = [h.strip().lower() for h in reader.fieldnames]
        missing_base = set(REQUIRED_BASE_COLS) - set(headers)
        if missing_base:
            raise AuditSchemaError(f"Missing required columns: {missing_base}")

        area_col = next((c for c in AREA_COLS if c in headers), None)
        if area_col is None:
            raise AuditSchemaError(f"Must include one of {AREA_COLS} to identify rating area(s).")

        for line_no, row in enumerate(reader, start=2):  # header is line 1
            total += 1
            normalized = {
                k.strip().lower(): (v or "").strip() for k, v in row.items() if k is not None
            }
            row_ok = True

            carrier = normalized.get("carrier_name", "")
            if not carrier:
                findings.append((line_no, "Missing carrier_name"))
                row_ok = False

            raw_change = normalized.get("approved_rate_change", "")
            clean_val = re.sub(r"[^\d.\-]", "", raw_change)
            try:
                rate = Decimal(clean_val) if clean_val else None
                if rate is None:
                    raise InvalidOperation
                if rate < MIN_SANE_RATE_CHANGE or rate > MAX_SANE_RATE_CHANGE:
                    findings.append(
                        (line_no, f"Rate {rate}% outside sane bounds "
                                  f"[{MIN_SANE_RATE_CHANGE}, {MAX_SANE_RATE_CHANGE}]")
                    )
                    row_ok = False
            except InvalidOperation:
                findings.append((line_no, f"Unparseable approved_rate_change: '{raw_change}'"))
                row_ok = False

            raw_area_field = normalized.get(area_col, "")
            areas: List[str] = []
            if area_col == "rating_area":
                if raw_area_field:
                    areas = [raw_area_field]
            else:
                try:
                    areas = parse_rating_areas(raw_area_field)
                except ValueError as e:
                    findings.append(
                        (line_no, f"Could not parse '{area_col}' value '{raw_area_field}': {e}")
                    )
                    row_ok = False

            if row_ok and not areas:
                findings.append((line_no, f"No rating area specified in '{area_col}'"))
                row_ok = False

            bad_areas = [a for a in areas if a not in valid_areas]
            if bad_areas:
                findings.append((line_no, f"Rating area(s) not found in crosswalk: {bad_areas}"))
                row_ok = False

            if row_ok:
                valid += 1

    return {
        "total_rows": total,
        "valid_rows": valid,
        "findings": findings,
        "counties_loaded": len(county_map),
    }


def main():
    try:
        result = audit_carrier_rates()
    except AuditSchemaError as e:
        print(f"[FAIL] Schema or file error: {e}")
        sys.exit(1)

    print(f"Loaded {result['counties_loaded']} counties from crosswalk.")
    print(f"Checked {result['total_rows']} carrier filing rows.")

    if result["findings"]:
        print(f"\n[FAIL] {len(result['findings'])} finding(s):")
        for line_no, msg in result["findings"]:
            print(f"  Line {line_no}: {msg}")
        sys.exit(1)

    print(f"\n[PASSED] All {result['valid_rows']} rows structurally valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()

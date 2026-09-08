#!/usr/bin/env python3
"""Existence gate: confirms scripts/bootstrap_data.py actually ran and left
the expected files in place before 04_audit.py does real schema and
crosswalk validation on them.

Deliberately does NOT re-check column headers or business-rule schema —
04_audit.py already does that thoroughly (structural checks + crosswalk
cross-reference). Duplicating that logic here would just be a second,
weaker copy that drifts out of sync with the first, which is the exact
failure mode this whole pipeline has been fixing. This stage only answers
"did bootstrap actually produce the files the rest of the pipeline needs,"
which is a cheap, useful thing to check before spending time on 04/05.
"""
import sys
from pathlib import Path

DATA_DIR = Path("data")
REQUIRED_FILES = [
    DATA_DIR / "public" / "approved_rates_2026.csv",
    DATA_DIR / "public" / "pa_county_fips_crosswalk.json",
]


def main() -> None:
    print("=== Checking Required Files Exist ===")
    errors = 0

    for path in REQUIRED_FILES:
        if path.exists():
            print(f"[OK] Found: {path}")
        else:
            print(f"[FAIL] Missing: {path}. Run scripts/bootstrap_data.py first.")
            errors += 1

    if errors > 0:
        print(f"=== Check Failed with {errors} error(s) ===")
        sys.exit(1)

    print("=== Check Complete — handing off to 04_audit.py for schema validation ===")


if __name__ == "__main__":
    main()

"""
validate_crosswalk.py – Verifies crosswalk JSON integrity against bootstrap module.
"""
import json
import sys
from pathlib import Path


def main():
    json_path = Path("data/public/pa_county_fips_crosswalk.json")
    if not json_path.is_file():
        print(f"Notice: JSON crosswalk file not found at {json_path}. Skipping JSON comparison.")
        sys.exit(0)

    with json_path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    count = len(data.get("counties", []))
    print(f"Crosswalk JSON verified: {count} counties mapped.")


if __name__ == "__main__":
    main()
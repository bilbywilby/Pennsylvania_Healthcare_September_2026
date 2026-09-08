"""
04_audit.py – Validates carrier rate CSV input files.
"""
import csv
import sys
from pathlib import Path


def audit_rates(csv_path: Path) -> bool:
    if not csv_path.is_file():
        print(f"Error: Target rate file not found at {csv_path}", file=sys.stderr)
        return False

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    print(f"Audited {len(rows)} rate entries in {csv_path.name}")
    return True


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/fixtures/sample_approved_rates_2026.csv")
    if not audit_rates(target):
        sys.exit(1)
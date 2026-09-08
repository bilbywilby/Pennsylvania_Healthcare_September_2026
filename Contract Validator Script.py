"""
contract_validator.py – Verifies repository contracts and environment setup.
"""
import sys
from pathlib import Path


def validate_contracts() -> bool:
    handover = Path("HANDOVER.json")
    if not handover.is_file():
        print("[-] HANDOVER.json missing", file=sys.stderr)
        return False
    return True


if __name__ == "__main__":
    if not validate_contracts():
        sys.exit(1)
    print("Repository contract validation passed.")
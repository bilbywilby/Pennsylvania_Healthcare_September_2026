#!/usr/bin/env python3
"""Small terminal front door for the Pennsylvania healthcare audit pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
WIKI_DIR = ROOT / "docs" / "wiki"


@dataclass(frozen=True)
class Check:
    label: str
    path: Path


def pipeline_scripts(root: Path = ROOT) -> list[Path]:
    """Return numbered pipeline stages in execution order."""
    return sorted(root.glob("[0-9][0-9]_*.py"))


def health_checks(root: Path = ROOT) -> list[Check]:
    """Return the small set of files that indicate a usable checkout."""
    return [
        Check("approved rates", root / "data" / "public" / "approved_rates_2026.csv"),
        Check("county crosswalk", root / "data" / "public" / "pa_county_fips_crosswalk.json"),
        Check("wiki index", root / "docs" / "wiki" / "index.md"),
    ]


def print_health(root: Path = ROOT) -> bool:
    """Print repository health and return whether every check passes."""
    checks = health_checks(root)
    passed = True
    print("\nRepository health")
    for check in checks:
        exists = check.path.exists()
        marker = "OK" if exists else "--"
        print(f"  [{marker}] {check.label}: {check.path.relative_to(root)}")
        if not exists and check.label == "approved rates":
            source = root / "approved_rates_2026.csv"
            if source.exists():
                print(f"       Source candidate found at {source.relative_to(root)}")
        passed = passed and exists
    return passed


def run_pipeline(root: Path = ROOT) -> int:
    """Run each numbered stage and stream its output to the terminal."""
    scripts = pipeline_scripts(root)
    if not scripts:
        print("No numbered pipeline scripts were found.", file=sys.stderr)
        return 1

    print("\nRunning audit pipeline")
    for script in scripts:
        print(f"\n>>> {script.name}")
        result = subprocess.run([sys.executable, str(script)], cwd=root, check=False)
        if result.returncode:
            print(f"Pipeline stopped at {script.name} (exit {result.returncode}).")
            return result.returncode
    print("\nPipeline completed successfully.")
    return 0


def wiki_pages(root: Path = ROOT) -> list[Path]:
    """Return Markdown wiki pages, with the index first when present."""
    pages = sorted((root / "docs" / "wiki").glob("*.md"))
    index = root / "docs" / "wiki" / "index.md"
    return ([index] if index in pages else []) + [page for page in pages if page != index]


def search_wiki(term: str, pages: Iterable[Path], root: Path = ROOT) -> int:
    """Print matching wiki lines and return the number of matches."""
    needle = term.casefold()
    matches = 0
    for page in pages:
        for line_number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if needle in line.casefold():
                print(f"{page.relative_to(root)}:{line_number}: {line.strip()}")
                matches += 1
    if not matches:
        print(f"No wiki matches for '{term}'.")
    return matches


def browse_wiki(root: Path = ROOT) -> None:
    pages = wiki_pages(root)
    if not pages:
        print("No wiki pages found yet. Add Markdown files under docs/wiki/.")
        return
    print("\nWiki pages")
    for number, page in enumerate(pages, 1):
        print(f"  {number}. {page.stem}")
    choice = input("Open page number (Enter to cancel): ").strip()
    if not choice:
        return
    try:
        page = pages[int(choice) - 1]
    except (ValueError, IndexError):
        print("Please choose one of the listed page numbers.")
        return
    print(f"\n--- {page.relative_to(root)} ---\n")
    print(page.read_text(encoding="utf-8"))


def interactive(root: Path = ROOT) -> int:
    while True:
        print("\nPennsylvania Health Audit")
        print("  1. Run audit pipeline")
        print("  2. Check repository health")
        print("  3. Browse wiki")
        print("  4. Search wiki")
        print("  q. Quit")
        choice = input("Select an action: ").strip().casefold()
        if choice == "1":
            run_pipeline(root)
        elif choice == "2":
            print_health(root)
        elif choice == "3":
            browse_wiki(root)
        elif choice == "4":
            term = input("Search term: ").strip()
            if term:
                search_wiki(term, wiki_pages(root), root)
        elif choice in {"q", "quit", "exit"}:
            return 0
        else:
            print("Choose 1, 2, 3, 4, or q.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Terminal interface for the PA health audit pipeline")
    parser.add_argument("--run", action="store_true", help="run the numbered audit pipeline")
    parser.add_argument("--health", action="store_true", help="check required repository files")
    parser.add_argument("--search", metavar="TERM", help="search Markdown pages under docs/wiki")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.run:
        return run_pipeline()
    if args.health:
        return 0 if print_health() else 1
    if args.search:
        return 0 if search_wiki(args.search, wiki_pages()) else 1
    return interactive()


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""
Pennsylvania Provenance Engine - Main CLI Entry Point.
Integrates auditing, validation, and report generation workflows.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Ensure local imports work whether executed directly or via module path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Config
from src.provenance_engine.auditor import MarketAuditor
from src.provenance_engine.validator import RateValidator
from src.provenance_engine.reporter import ReportGenerator


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Pennsylvania Provenance Engine - Audit & Validate Health Insurance Rate Data"
    )
    parser.add_argument(
        "--data-file",
        type=str,
        default="data/sample_2026_data.json",
        help="Path to external JSON data file (optional)."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=20.0,
        help="Percentage threshold for high-risk carrier designation (default: 20.0)."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save the generated report output file."
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Export summary and validation output as structured JSON instead of formatted text."
    )
    return parser.parse_args()


def load_external_data(filepath: str) -> Dict[str, Any]:
    """Helper to load sample or user-provided JSON data."""
    path = Path(filepath)
    if not path.exists():
        print(f"[!] Warning: Data file '{filepath}' not found. Using default Config dataset.", file=sys.stderr)
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as err:
        print(f"[!] Error reading JSON data file: {err}", file=sys.stderr)
        return {}


def main() -> None:
    """Main execution workflow."""
    args = parse_args()

    print(f"==================================================")
    print(f" Starting {Config.APP_NAME} (v{Config.VERSION})")
    print(f" Audit Target Year: {Config.AUDIT_YEAR}")
    print(f"==================================================")

    # Load custom dataset if available
    external_data = load_external_data(args.data_file)
    
    # Instantiate Auditor
    auditor = MarketAuditor()
    
    # If external data provided, override default carrier dicts if present
    if "carriers" in external_data:
        if "2026" in external_data["carriers"]:
            auditor.carriers_2026 = external_data["carriers"]["2026"]
        if "2027_requests" in external_data["carriers"]:
            auditor.carriers_2027 = external_data["carriers"]["2027_requests"]

    # Run Audit Summary
    summary = auditor.generate_summary_report()
    
    # Recalculate high risk carriers based on CLI threshold parameter
    high_risk_carriers = auditor.get_high_risk_carriers(threshold=args.threshold)
    summary["statistics"]["high_risk_threshold_pct"] = args.threshold
    summary["statistics"]["high_risk_carriers"] = high_risk_carriers
    summary["statistics"]["carriers_above_threshold"] = len(high_risk_carriers)

    # Instantiate and run Rate Validator
    validator = RateValidator(
        carriers_2026=auditor.carriers_2026,
        carriers_2027=auditor.carriers_2027
    )
    validation_results = validator.run_validation()

    # Format Output Report
    if args.json_output:
        report_content = json.dumps(
            {
                "summary": summary,
                "validation": validation_results
            },
            indent=2
        )
    else:
        reporter = ReportGenerator(summary=summary, validation=validation_results)
        report_content = reporter.generate_text_report()

    # Output Handling (File vs stdout)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"[✓] Audit report successfully written to: {output_path.resolve()}")
    else:
        print("\n" + report_content)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Integration tests for bootstrap/04_audit.py (carrier rate filing auditor).
"""
import csv
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent.parent / "bootstrap" / "04_audit.py"

spec = importlib.util.spec_from_file_location("audit_module", MODULE_PATH)
audit_module = importlib.util.module_from_spec(spec)
sys.modules["audit_module"] = audit_module
spec.loader.exec_module(audit_module)


class BaseAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.temp_dir) / "data"
        self.public_dir = self.data_dir / "public"
        self.public_dir.mkdir(parents=True)

        # Minimal crosswalk covering areas 1-9, one county each (enough for
        # rating-area membership checks; audit doesn't need full 67 counties).
        crosswalk_data = {
            str(area): [{"county": f"County{area}", "fips": f"4200{area}"}]
            for area in range(1, 10)
        }
        with open(self.public_dir / "pa_county_fips_crosswalk.json", "w") as f:
            json.dump(crosswalk_data, f)

        self._orig = {
            "CARRIER_RATES_FILE": audit_module.CARRIER_RATES_FILE,
            "CROSSWALK_FILE": audit_module.CROSSWALK_FILE,
        }
        audit_module.CARRIER_RATES_FILE = self.data_dir / "public" / "approved_rates_2026.csv"
        audit_module.CROSSWALK_FILE = self.public_dir / "pa_county_fips_crosswalk.json"

    def tearDown(self):
        for key, value in self._orig.items():
            setattr(audit_module, key, value)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def write_rates(self, content: str):
        with open(audit_module.CARRIER_RATES_FILE, "w", encoding="utf-8") as f:
            f.write(content)


class TestSchemaErrors(BaseAuditTest):
    def test_missing_file_raises_schema_error(self):
        with self.assertRaises(audit_module.AuditSchemaError):
            audit_module.audit_carrier_rates()

    def test_missing_carrier_name_column_raises_schema_error(self):
        self.write_rates("approved_rate_change,rating_area\n10.0,1\n")
        with self.assertRaises(audit_module.AuditSchemaError):
            audit_module.audit_carrier_rates()

    def test_missing_area_column_raises_schema_error(self):
        self.write_rates("carrier_name,approved_rate_change\nHighmark,10.0\n")
        with self.assertRaises(audit_module.AuditSchemaError):
            audit_module.audit_carrier_rates()

    def test_missing_crosswalk_raises_schema_error(self):
        audit_module.CROSSWALK_FILE.unlink()
        self.write_rates("carrier_name,approved_rate_change,rating_area\nHighmark,10.0,1\n")
        with self.assertRaises(audit_module.AuditSchemaError):
            audit_module.audit_carrier_rates()


class TestStructuralFindings(BaseAuditTest):
    def test_valid_row_with_bare_rating_area_passes(self):
        self.write_rates("carrier_name,approved_rate_change,rating_area\nHighmark,17.7,1\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(result["valid_rows"], 1)
        self.assertEqual(result["findings"], [])

    def test_valid_rows_with_primary_rating_areas_range_and_list(self):
        self.write_rates(
            "carrier_name,approved_rate_change,primary_rating_areas\n"
            "Ambetter,37.8,1-9\n"
            "Keystone Health Plan Central,22.4,6;7;9\n"
        )
        result = audit_module.audit_carrier_rates()
        self.assertEqual(result["total_rows"], 2)
        self.assertEqual(result["findings"], [])

    def test_missing_carrier_name_is_a_finding(self):
        self.write_rates("carrier_name,approved_rate_change,rating_area\n,10.0,1\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("Missing carrier_name", result["findings"][0][1])

    def test_unparseable_rate_is_a_finding(self):
        self.write_rates("carrier_name,approved_rate_change,rating_area\nHighmark,not-a-number,1\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("Unparseable", result["findings"][0][1])

    def test_rate_outside_sane_bounds_is_a_finding(self):
        self.write_rates("carrier_name,approved_rate_change,rating_area\nHighmark,250.0,1\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("outside sane bounds", result["findings"][0][1])

    def test_negative_rate_within_bounds_passes(self):
        self.write_rates("carrier_name,approved_rate_change,rating_area\nPartners,-10.1,1\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(result["valid_rows"], 1)

    def test_unknown_rating_area_is_a_finding(self):
        self.write_rates("carrier_name,approved_rate_change,rating_area\nHighmark,10.0,99\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("not found in crosswalk", result["findings"][0][1])

    def test_unparseable_primary_rating_areas_is_a_finding(self):
        self.write_rates("carrier_name,approved_rate_change,primary_rating_areas\nHighmark,10.0,north\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(len(result["findings"]), 1)
        self.assertIn("Could not parse", result["findings"][0][1])

    def test_row_with_multiple_problems_reports_once_but_excluded(self):
        # Bad rate AND bad area on the same row: still just one row excluded
        # from valid_rows, though it may produce more than one finding line.
        self.write_rates("carrier_name,approved_rate_change,rating_area\n,bad,99\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(result["valid_rows"], 0)
        self.assertGreaterEqual(len(result["findings"]), 2)


class TestFlatListCrosswalkSchema(unittest.TestCase):
    """The crosswalk shape produced by scripts/bootstrap_data.py."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.temp_dir) / "data"
        self.public_dir = self.data_dir / "public"
        self.public_dir.mkdir(parents=True)

        flat_crosswalk = {
            "state_fips": "42",
            "state_abbr": "PA",
            "counties": [
                {"fips": "42003", "canonical_name": "Allegheny", "rating_area": 4},
                {"fips": "42049", "canonical_name": "Erie", "rating_area": 1},
            ],
        }
        with open(self.public_dir / "pa_county_fips_crosswalk.json", "w") as f:
            json.dump(flat_crosswalk, f)

        self._orig = {
            "CARRIER_RATES_FILE": audit_module.CARRIER_RATES_FILE,
            "CROSSWALK_FILE": audit_module.CROSSWALK_FILE,
        }
        audit_module.CARRIER_RATES_FILE = self.data_dir / "public" / "approved_rates_2026.csv"
        audit_module.CROSSWALK_FILE = self.public_dir / "pa_county_fips_crosswalk.json"

    def tearDown(self):
        for key, value in self._orig.items():
            setattr(audit_module, key, value)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_flat_schema_crosswalk_loads_and_validates(self):
        with open(audit_module.CARRIER_RATES_FILE, "w", encoding="utf-8") as f:
            f.write("carrier_name,approved_rate_change,rating_area\nHighmark,17.7,4\n")
        result = audit_module.audit_carrier_rates()
        self.assertEqual(result["valid_rows"], 1)
        self.assertEqual(result["counties_loaded"], 2)


class TestRealBootstrapData(unittest.TestCase):
    """Regression test against the exact file scripts/bootstrap_data.py
    generates — catches drift between this validator and the real schema."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.temp_dir) / "data"
        self.public_dir = self.data_dir / "public"
        self.public_dir.mkdir(parents=True)

        crosswalk_data = {
            str(area): [{"county": f"County{area}", "fips": f"4200{area}"}]
            for area in range(1, 10)
        }
        with open(self.public_dir / "pa_county_fips_crosswalk.json", "w") as f:
            json.dump(crosswalk_data, f)

        real_rates = (
            "carrier_name,approved_rate_change,market_segment,primary_rating_areas\n"
            "Ambetter (Centene),+37.8%,Individual,1-9\n"
            "Keystone Health Plan Central,+22.4%,Individual,6;7;9\n"
            "Keystone Health Plan East,+22.0%,Individual,8\n"
            "UPMC Health Plan,+24.8%,Individual,1;4;5\n"
            "Highmark Inc.,+17.7%,Individual,1;2;4;5;6;7;9\n"
            "Highmark Benefits Group,+18.4%,Individual,3;8\n"
            "Geisinger Health Plan,+11.6%,Individual,2;3;5;6;7;9\n"
            "Capital Advantage Assurance,+24.6%,Individual,6;7;9\n"
            "Partners Insurance Co.,-10.1%,Individual,3;6;8\n"
        )
        self.rates_file = self.public_dir / "approved_rates_2026.csv"
        self.rates_file.write_text(real_rates, encoding="utf-8")

        self._orig = {
            "CARRIER_RATES_FILE": audit_module.CARRIER_RATES_FILE,
            "CROSSWALK_FILE": audit_module.CROSSWALK_FILE,
        }
        audit_module.CARRIER_RATES_FILE = self.rates_file
        audit_module.CROSSWALK_FILE = self.public_dir / "pa_county_fips_crosswalk.json"

    def tearDown(self):
        for key, value in self._orig.items():
            setattr(audit_module, key, value)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_real_bootstrap_data_passes_cleanly(self):
        result = audit_module.audit_carrier_rates()
        self.assertEqual(result["total_rows"], 9)
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["valid_rows"], 9)


if __name__ == "__main__":
    unittest.main()

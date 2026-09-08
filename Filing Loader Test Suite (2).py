import sys
from pathlib import Path

# Path bootstrap for standalone execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import pytest
import schema_reconciliation as sr

def test_validated_filings_flow_through_exposure():
    """Integration bridge proving validated filings schema compatibility with exposure calculation."""
    validated = sr.validate_filings([
        {"carrier": "Carrier A", "serff_id": "CARA-000000001", "rating_areas": [1],
         "rate_change": 10.0, "lives_by_area": {1: 100.0}, "verified": True},
        {"carrier": "Carrier B", "serff_id": "CARB-000000002", "rating_areas": [1],
         "rate_change": 20.0, "lives_by_area": {1: 300.0}, "verified": True},
    ])
    exposure = sr.compute_rating_area_exposure(validated)
    assert exposure[1]["weighted_rate_change"] == 17.50
    assert exposure[1]["verified"] is True

def test_unverified_row_poisons_group_verification_status(tmp_path):
    """Any unverified row within a serff-group poisons the group's verified flag."""
    csv_content = (
        "carrier,serff_id,rate_change,rating_area,covered_lives,verified\n"
        "Carrier A,CARA-000000001,10.0,1,100,True\n"
        "Carrier A,CARA-000000001,12.0,1,200,False\n"
    )
    p = tmp_path / "carrier-rate-changes.csv"
    p.write_text(csv_content)

    records = sr.load_filings_from_csv(p)

    # Rows group by serff_id BEFORE validation, so same-ID rows merge;
    # the unverified row poisons the merged record.
    assert len(records) == 1
    assert records[0]["verified"] is False

    exposure = sr.compute_rating_area_exposure(records)
    # Weighted average: (10.0 * 100 + 12.0 * 200) / 300 = 11.33
    assert exposure[1]["weighted_rate_change"] == round((10.0 * 100 + 12.0 * 200) / 300, 2)
    assert exposure[1]["verified"] is False

def test_legacy_column_names_are_normalized(tmp_path):
    """Ensure legacy column spellings (carrier_name, approved_rate_change) normalize to canonical keys."""
    p = tmp_path / "legacy.csv"
    p.write_text(
        "carrier_name,approved_rate_change,rating_area\n"
        "Highmark,17.75,4\n"
    )
    records = sr.load_filings_from_csv(p)
    assert records and records[0]["carrier"] == "Highmark"
    assert records[0]["rate_change"] == 17.75
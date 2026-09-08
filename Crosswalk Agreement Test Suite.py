import csv
import json
from pathlib import Path
import pytest
from bootstrap.pa_crosswalk_data import (
    PA_RATING_AREA_MAP,
    EXPECTED_COUNTY_COUNT,
    VALID_RATING_AREAS,
)


def test_pa_crosswalk_completeness_and_bounds():
    """Verify that canonical crosswalk contains all 67 PA counties mapped to areas 1-9."""
    assert len(PA_RATING_AREA_MAP) == EXPECTED_COUNTY_COUNT, (
        f"Expected {EXPECTED_COUNTY_COUNT} counties, found {len(PA_RATING_AREA_MAP)}"
    )

    for county, rating_area in PA_RATING_AREA_MAP.items():
        assert isinstance(county, str) and len(county) > 0
        assert rating_area in VALID_RATING_AREAS, (
            f"County '{county}' mapped to invalid area {rating_area}"
        )


def test_crosswalk_csv_parity_if_present(tmp_path):
    """Assert county-for-county parity against rating_areas_2026.csv when present."""
    possible_csv_paths = [
        Path("data/rating_areas_2026.csv"),
        Path("pa-audit-work/pennsylvania-health-insurance-audit-2026/data/rating_areas_2026.csv"),
    ]

    csv_path = next((p for p in possible_csv_paths if p.exists()), None)
    if csv_path is None:
        pytest.skip("rating_areas_2026.csv not found in expected repository locations.")

    csv_mappings = {}
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            county = row["county"].strip().title()
            area = int(row["rating_area"])
            csv_mappings[county] = area

    assert len(csv_mappings) == EXPECTED_COUNTY_COUNT
    for county, expected_area in PA_RATING_AREA_MAP.items():
        assert county in csv_mappings, f"County '{county}' missing from {csv_path}"
        assert csv_mappings[county] == expected_area, (
            f"Discrepancy in '{county}': Canonical map has {expected_area}, "
            f"CSV has {csv_mappings[county]}"
        )
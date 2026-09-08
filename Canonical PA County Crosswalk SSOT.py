"""
bootstrap/pa_crosswalk_data.py – Canonical Pennsylvania County Crosswalk SSOT
Defines the authoritative 67-county mapping for Pennsylvania, linking FIPS codes,
county names, and PA Insurance Department (PID) Rating Areas (1-9).
"""
from typing import Dict, List, TypedDict

class CountyEntry(TypedDict):
    fips: str
    county: str
    rating_area: int

# Authoritative 67 PA Counties mapping (FIPS 42xxx)
PA_COUNTIES_CANONICAL: List[CountyEntry] = [
    # Rating Area 1 (Northwest / Western PA)
    {"fips": "42005", "county": "Armstrong", "rating_area": 1},
    {"fips": "42001", "county": "Adams", "rating_area": 6},
    {"fips": "42003", "county": "Allegheny", "rating_area": 2},
    {"fips": "42007", "county": "Beaver", "rating_area": 1},
    {"fips": "42009", "county": "Bedford", "rating_area": 7},
    {"fips": "42011", "county": "Berks", "rating_area": 6},
    {"fips": "42013", "county": "Blair", "rating_area": 7},
    {"fips": "42015", "county": "Bradford", "rating_area": 4},
    {"fips": "42017", "county": "Bucks", "rating_area": 9},
    {"fips": "42019", "county": "Butler", "rating_area": 1},
    {"fips": "42021", "county": "Cambria", "rating_area": 7},
    {"fips": "42023", "county": "Cameron", "rating_area": 3},
    {"fips": "42025", "county": "Carbon", "rating_area": 8},
    {"fips": "42027", "county": "Centre", "rating_area": 5},
    {"fips": "42029", "county": "Chester", "rating_area": 9},
    {"fips": "42031", "county": "Clarion", "rating_area": 1},
    {"fips": "42033", "county": "Clearfield", "rating_area": 3},
    {"fips": "42035", "county": "Clinton", "rating_area": 4},
    {"fips": "42037", "county": "Columbia", "rating_area": 5},
    {"fips": "42039", "county": "Crawford", "rating_area": 1},
    {"fips": "42041", "county": "Cumberland", "rating_area": 6},
    {"fips": "42043", "county": "Dauphin", "rating_area": 6},
    {"fips": "42045", "county": "Delaware", "rating_area": 9},
    {"fips": "42047", "county": "Elk", "rating_area": 3},
    {"fips": "42049", "county": "Erie", "rating_area": 1},
    {"fips": "42051", "county": "Fayette", "rating_area": 2},
    {"fips": "42053", "county": "Forest", "rating_area": 1},
    {"fips": "42055", "county": "Franklin", "rating_area": 6},
    {"fips": "42057", "county": "Fulton", "rating_area": 7},
    {"fips": "42059", "county": "Greene", "rating_area": 2},
    {"fips": "42061", "county": "Huntingdon", "rating_area": 7},
    {"fips": "42063", "county": "Indiana", "rating_area": 2},
    {"fips": "42065", "county": "Jefferson", "rating_area": 3},
    {"fips": "42067", "county": "Juniata", "rating_area": 7},
    {"fips": "42069", "county": "Lackawanna", "rating_area": 8},
    {"fips": "42071", "county": "Lancaster", "rating_area": 6},
    {"fips": "42073", "county": "Lawrence", "rating_area": 1},
    {"fips": "42075", "county": "Lebanon", "rating_area": 6},
    {"fips": "42077", "county": "Lehigh", "rating_area": 6},
    {"fips": "42079", "county": "Luzerne", "rating_area": 8},
    {"fips": "42081", "county": "Lycoming", "rating_area": 4},
    {"fips": "42083", "county": "McKean", "rating_area": 3},
    {"fips": "42085", "county": "Mercer", "rating_area": 1},
    {"fips": "42087", "county": "Mifflin", "rating_area": 7},
    {"fips": "42089", "county": "Monroe", "rating_area": 8},
    {"fips": "42091", "county": "Montgomery", "rating_area": 9},
    {"fips": "42093", "county": "Montour", "rating_area": 5},
    {"fips": "42095", "county": "Northampton", "rating_area": 6},
    {"fips": "42097", "county": "Northumberland", "rating_area": 5},
    {"fips": "42099", "county": "Perry", "rating_area": 6},
    {"fips": "42101", "county": "Philadelphia", "rating_area": 9},
    {"fips": "42103", "county": "Pike", "rating_area": 8},
    {"fips": "42105", "county": "Potter", "rating_area": 3},
    {"fips": "42107", "county": "Schuylkill", "rating_area": 6},
    {"fips": "42109", "county": "Snyder", "rating_area": 5},
    {"fips": "42111", "county": "Somerset", "rating_area": 7},
    {"fips": "42113", "county": "Sullivan", "rating_area": 4},
    {"fips": "42115", "county": "Susquehanna", "rating_area": 8},
    {"fips": "42117", "county": "Tioga", "rating_area": 4},
    {"fips": "42119", "county": "Union", "rating_area": 5},
    {"fips": "42121", "county": "Venango", "rating_area": 1},
    {"fips": "42123", "county": "Warren", "rating_area": 1},
    {"fips": "42125", "county": "Washington", "rating_area": 2},
    {"fips": "42127", "county": "Wayne", "rating_area": 8},
    {"fips": "42129", "county": "Westmoreland", "rating_area": 2},
    {"fips": "42131", "county": "Wyoming", "rating_area": 8},
    {"fips": "42133", "county": "York", "rating_area": 6},
]

_seen_fips = set()
_seen_counties = set()
_clean_counties = []

for entry in PA_COUNTIES_CANONICAL:
    if entry["fips"] not in _seen_fips:
        _seen_fips.add(entry["fips"])
        _seen_counties.add(entry["county"])
        _clean_counties.append(entry)

PA_COUNTIES_CLEAN = _clean_counties

assert len(PA_COUNTIES_CLEAN) == 67, f"Expected 67 unique county entries, got {len(PA_COUNTIES_CLEAN)}"
assert len(_seen_counties) == 67, f"Expected 67 unique county names, got {len(_seen_counties)}"
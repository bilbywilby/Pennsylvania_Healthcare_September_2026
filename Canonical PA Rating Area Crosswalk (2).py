"""
Canonical Pennsylvania ACA Rating Area Crosswalk Data (CMS Standard).

Defines the authoritative 67-county mapping for PA Rating Areas 1 through 9
in accordance with CMS Geographic Rating Area guidelines.
"""

PA_RATING_AREA_MAP = {
    # Area 1: Northwest Pennsylvania (8 counties)
    "Clarion": 1,
    "Crawford": 1,
    "Erie": 1,
    "Forest": 1,
    "McKean": 1,
    "Mercer": 1,
    "Venango": 1,
    "Warren": 1,

    # Area 2: North Central Pennsylvania (3 counties)
    "Cameron": 2,
    "Elk": 2,
    "Potter": 2,

    # Area 3: Northeast Pennsylvania / Poconos (13 counties)
    "Bradford": 3,
    "Carbon": 3,
    "Clinton": 3,
    "Lackawanna": 3,
    "Luzerne": 3,
    "Lycoming": 3,
    "Monroe": 3,
    "Pike": 3,
    "Sullivan": 3,
    "Susquehanna": 3,
    "Tioga": 3,
    "Wayne": 3,
    "Wyoming": 3,

    # Area 4: Pittsburgh Metro & Western PA (10 counties)
    "Allegheny": 4,
    "Armstrong": 4,
    "Beaver": 4,
    "Butler": 4,
    "Fayette": 4,
    "Greene": 4,
    "Indiana": 4,
    "Lawrence": 4,
    "Washington": 4,
    "Westmoreland": 4,

    # Area 5: Central West / Alleghenies (7 counties)
    "Bedford": 5,
    "Blair": 5,
    "Cambria": 5,
    "Clearfield": 5,
    "Huntingdon": 5,
    "Jefferson": 5,
    "Somerset": 5,

    # Area 6: Susquehanna Valley & Lehigh (10 counties)
    "Centre": 6,
    "Columbia": 6,
    "Lehigh": 6,
    "Mifflin": 6,
    "Montour": 6,
    "Northampton": 6,
    "Northumberland": 6,
    "Schuylkill": 6,
    "Snyder": 6,
    "Union": 6,

    # Area 7: South Central Pennsylvania (4 counties)
    "Adams": 7,
    "Berks": 7,
    "Lancaster": 7,
    "York": 7,

    # Area 8: Philadelphia Metro (5 counties)
    "Bucks": 8,
    "Chester": 8,
    "Delaware": 8,
    "Montgomery": 8,
    "Philadelphia": 8,

    # Area 9: Cumberland Valley & Central South (7 counties)
    "Cumberland": 9,
    "Dauphin": 9,
    "Franklin": 9,
    "Fulton": 9,
    "Juniata": 9,
    "Lebanon": 9,
    "Perry": 9,
}

EXPECTED_COUNTY_COUNT = 67
VALID_RATING_AREAS = set(range(1, 10))


def get_rating_area(county_name: str) -> int:
    """Return the 1-based rating area for a given Pennsylvania county."""
    normalized = county_name.strip().title()
    if normalized not in PA_RATING_AREA_MAP:
        raise KeyError(f"Invalid or unmapped Pennsylvania county: '{county_name}'")
    return PA_RATING_AREA_MAP[normalized]
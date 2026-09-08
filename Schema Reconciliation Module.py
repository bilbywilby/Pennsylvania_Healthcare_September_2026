"""
Schema Reconciliation & Rating Area Exposure Calculation Module.

Provides normalized filing validation, rating area exposure calculation,
unweighted fallback mechanics, and county rate matrix generation.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_crosswalk(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load Pennsylvania county rating area crosswalk."""
    if path is not None and Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    default_path = Path("data/pa_crosswalk.json")
    if default_path.exists():
        with open(default_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Fallback to canonical python dictionary if JSON artifact missing
    try:
        from bootstrap.pa_crosswalk_data import PA_RATING_AREA_MAP
        return PA_RATING_AREA_MAP
    except ImportError:
        return {}


def validate_filings(filings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validate and normalize filing data structures.

    Ensures carrier names, rate changes, rating area lists, covered lives maps,
    and verification flags adhere to canonical schema types.
    """
    validated = []
    for f in filings:
        record = dict(f)

        # Normalize carrier name
        carrier = record.get("carrier") or record.get("carrier_name", "")
        if not carrier:
            raise ValueError("Missing required carrier name in filing record.")
        record["carrier"] = str(carrier).strip()

        # Normalize rate change
        raw_rate = record.get("rate_change") if "rate_change" in record else record.get("approved_rate_change")
        if raw_rate is None:
            raise ValueError(f"Missing rate_change for carrier '{carrier}'")
        try:
            record["rate_change"] = float(raw_rate)
        except (ValueError, TypeError):
            raise ValueError(f"Unparseable numeric rate_change '{raw_rate}' for carrier '{carrier}'")

        # Normalize rating area(s)
        areas = []
        if "rating_areas" in record and record["rating_areas"]:
            r_areas = record["rating_areas"]
            if isinstance(r_areas, (list, tuple, set)):
                areas = [int(a) for a in r_areas]
            else:
                areas = [int(r_areas)]
        elif "rating_area" in record and record["rating_area"] is not None:
            r_area = record["rating_area"]
            if isinstance(r_area, (list, tuple, set)):
                areas = [int(a) for a in r_area]
            else:
                areas = [int(r_area)]
        record["rating_areas"] = areas
        record["rating_area"] = areas[0] if areas else None

        # Normalize covered lives / lives_by_area
        lives_map = {}
        if "lives_by_area" in record and isinstance(record["lives_by_area"], dict):
            lives_map = {int(k): float(v) for k, v in record["lives_by_area"].items()}
        elif "covered_lives" in record and record["covered_lives"] is not None:
            try:
                c_lives = float(record["covered_lives"])
                if areas:
                    for a in areas:
                        lives_map[a] = c_lives / len(areas)
            except (ValueError, TypeError):
                pass
        record["lives_by_area"] = lives_map

        # Normalize verification flag
        if "verified" in record:
            v_val = record["verified"]
            if isinstance(v_val, str):
                record["verified"] = v_val.strip().lower() in ("true", "1", "yes")
            else:
                record["verified"] = bool(v_val)
        else:
            record["verified"] = True

        validated.append(record)

    return validated


def compute_rating_area_exposure(filings: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Compute rating area rate changes weighted by covered lives.

    Falls back to simple unweighted average if covered lives are missing or 0.
    """
    area_data: Dict[int, List[Dict[str, Any]]] = {}

    for f in filings:
        areas = f.get("rating_areas", [])
        if not areas and f.get("rating_area") is not None:
            areas = [f["rating_area"]]

        rate = f.get("rate_change", 0.0)
        lives_map = f.get("lives_by_area", {})
        covered_lives_scalar = f.get("covered_lives")
        verified = f.get("verified", True)

        for a in areas:
            a_int = int(a)
            if a_int not in area_data:
                area_data[a_int] = []

            lives = 0.0
            if a_int in lives_map:
                lives = float(lives_map[a_int])
            elif covered_lives_scalar is not None:
                try:
                    lives = float(covered_lives_scalar) / len(areas)
                except (ValueError, TypeError, ZeroDivisionError):
                    lives = 0.0

            area_data[a_int].append({
                "rate": rate,
                "lives": lives,
                "verified": verified
            })

    exposure = {}
    all_areas = sorted(set(area_data.keys()).union(set(range(1, 10))))

    for a in all_areas:
        records = area_data.get(a, [])
        if not records:
            exposure[a] = {
                "weighted_rate_change": 0.0,
                "verified": True,
                "basis": "unweighted_fallback",
                "total_lives": 0.0
            }
            continue

        total_lives = sum(r["lives"] for r in records)
        all_verified = all(r["verified"] for r in records)

        if total_lives > 0:
            weighted_sum = sum(r["rate"] * r["lives"] for r in records)
            weighted_rate = round(weighted_sum / total_lives, 2)
            basis = "covered_lives"
        else:
            weighted_rate = round(sum(r["rate"] for r in records) / len(records), 2)
            basis = "unweighted_fallback"

        exposure[a] = {
            "weighted_rate_change": weighted_rate,
            "verified": all_verified,
            "basis": basis,
            "total_lives": total_lives
        }

    return exposure


def build_county_rate_matrix(filings: List[Dict[str, Any]], crosswalk: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    """Bind rating area rate exposure onto individual Pennsylvania county FIPS codes."""
    if crosswalk is None:
        crosswalk = load_crosswalk()

    exposure = compute_rating_area_exposure(filings)
    matrix = {}

    counties_list = []
    if isinstance(crosswalk, dict):
        if "counties" in crosswalk and isinstance(crosswalk["counties"], list):
            for c in crosswalk["counties"]:
                fips = str(c.get("fips") or c.get("county_fips") or c.get("county", ""))
                area = int(c.get("rating_area") or c.get("rating_area_id", 0))
                counties_list.append((fips, area, c))
        else:
            for k, v in crosswalk.items():
                if isinstance(v, dict):
                    area = int(v.get("rating_area") or v.get("rating_area_id") or 0)
                else:
                    area = int(v)
                counties_list.append((str(k), area, v))

    for fips, area, _ in counties_list:
        exp = exposure.get(area, {})
        w_rate = exp.get("weighted_rate_change", 0.0)
        matrix[fips] = {
            "fips": fips,
            "rating_area": area,
            "weighted_rate_change": w_rate,
            "rate_change": w_rate,
            "verified": exp.get("verified", True),
            "basis": exp.get("basis", "unweighted_fallback")
        }

    return matrix


def load_filings_from_csv(csv_path: Path) -> List[Dict[str, Any]]:
    """Load, merge, and validate filing records from a local CSV file."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Carrier rate CSV not found at: {csv_path}")

    raw_rows = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm_row = {}
            for k, v in row.items():
                if k is None:
                    continue
                key_clean = k.strip().lower()
                if key_clean in ("carrier", "carrier_name"):
                    norm_row["carrier"] = v.strip() if v else ""
                elif key_clean in ("rate_change", "approved_rate_change"):
                    norm_row["rate_change"] = v.strip() if v else "0.0"
                elif key_clean in ("rating_area", "rating_area_id"):
                    norm_row["rating_area"] = v.strip() if v else ""
                elif key_clean == "covered_lives":
                    norm_row["covered_lives"] = v.strip() if v else "0"
                elif key_clean == "serff_id":
                    norm_row["serff_id"] = v.strip() if v else ""
                elif key_clean == "verified":
                    norm_row["verified"] = v.strip() if v else "True"
                else:
                    norm_row[key_clean] = v.strip() if v else ""
            raw_rows.append(norm_row)

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    ungrouped = []
    for r in raw_rows:
        serff = r.get("serff_id")
        if serff:
            grouped.setdefault(serff, []).append(r)
        else:
            ungrouped.append(r)

    processed_filings = []

    # Merge grouped SERFF records (poisoning verified flag if any row is unverified)
    for serff, rows in grouped.items():
        carrier = rows[0]["carrier"]
        verified = all(r.get("verified", "True").lower() in ("true", "1", "yes") for r in rows)

        areas = set()
        lives_by_area = {}
        total_rate_sum = 0.0
        total_lives = 0.0

        for r in rows:
            area = int(r["rating_area"]) if r.get("rating_area") else None
            rate = float(r.get("rate_change", 0.0))
            lives = float(r.get("covered_lives", 0.0))

            if area is not None:
                areas.add(area)
                lives_by_area[area] = lives_by_area.get(area, 0.0) + lives
            total_rate_sum += rate * (lives if lives > 0 else 1.0)
            total_lives += lives

        weighted_rate = total_rate_sum / total_lives if total_lives > 0 else total_rate_sum / len(rows)

        processed_filings.append({
            "carrier": carrier,
            "serff_id": serff,
            "rating_areas": sorted(list(areas)),
            "rate_change": round(weighted_rate, 2),
            "lives_by_area": lives_by_area,
            "covered_lives": total_lives,
            "verified": verified
        })

    for r in ungrouped:
        verified = r.get("verified", "True").lower() in ("true", "1", "yes")
        area = int(r["rating_area"]) if r.get("rating_area") else None
        rate = float(r.get("rate_change", 0.0))
        lives = float(r.get("covered_lives", 0.0))

        processed_filings.append({
            "carrier": r.get("carrier", ""),
            "serff_id": r.get("serff_id", ""),
            "rating_areas": [area] if area else [],
            "rating_area": area,
            "rate_change": rate,
            "covered_lives": lives,
            "lives_by_area": {area: lives} if area else {},
            "verified": verified
        })

    return validate_filings(processed_filings)
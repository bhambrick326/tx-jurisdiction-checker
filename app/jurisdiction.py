import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from .config import CITY_LIMITS_PATH, PERMIT_LINKS_CSV

# Load data once
_city_limits: gpd.GeoDataFrame = gpd.read_file(CITY_LIMITS_PATH)
_permit_links: pd.DataFrame = pd.read_csv(PERMIT_LINKS_CSV)

def _extract_city_name(row: pd.Series) -> str:
    """
    Be flexible about the column name used for city/place in the dataset.
    """
    candidates = ["NAME", "NAME20", "CITY_NM", "CITYNAME", "CITY", "MUNICIPALI", "PLACE_NAME"]
    for col in candidates:
        if col in row.index and pd.notna(row[col]):
            return str(row[col])
    return "Unknown"

def _find_link(name: str) -> str | None:
    """
    Return a permit URL if we have one in the CSV.
    Falls back to 'Unincorporated County' if not found.
    """
    try:
        # Case-insensitive, partial match
        hits = _permit_links[_permit_links["Name"].str.contains(name, case=False, na=False)]
        if not hits.empty:
            url = hits.iloc[0]["Permit_URL"]
            return url if isinstance(url, str) and url.strip() else None
    except Exception:
        pass

    # Default fallback → Unincorporated County
    default = _permit_links[_permit_links["Name"].str.contains("Unincorporated", case=False, na=False)]
    if not default.empty:
        return default.iloc[0]["Permit_URL"]

    return None

def check_jurisdiction(lat: float, lon: float) -> dict:
    """
    Returns:
      Inside city limits:
        {"status":"inside","city":"Conroe","permit_url":"https://www.cityofconroe.org/services/building-permits"}

      Outside city limits:
        {"status":"outside","city":"Unincorporated County","permit_url":"https://www.texascountyclerk.org/permits"}
    """
    pt = Point(lon, lat)
    hit = _city_limits[_city_limits.contains(pt)]

    if not hit.empty:
        city = _extract_city_name(hit.iloc[0])
        return {
            "status": "inside",
            "city": city,
            "permit_url": _find_link(city)
        }

    # Outside → automatically Unincorporated County
    return {
        "status": "outside",
        "city": "Unincorporated County",
        "permit_url": _find_link("Unincorporated County")
    }

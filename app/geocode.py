import requests
from .config import MAPBOX_TOKEN

def geocode_address(address: str):
    """
    Use Mapbox API to convert an address into (lat, lon).
    Returns (lat, lon) or (None, None) if not found.
    """
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    params = {
        "access_token": MAPBOX_TOKEN,
        "limit": 1,
        "country": "US"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "features" in data and len(data["features"]) > 0:
        coords = data["features"][0]["geometry"]["coordinates"]
        lon, lat = coords  # Mapbox gives [lon, lat]
        return lat, lon

    return None, None

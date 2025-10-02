import requests
import os

def geocode_address(address):
    mapbox_token = os.getenv("MAPBOX_TOKEN")
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    params = {
        "access_token": mapbox_token,
        "limit": 1,
        "country": "US"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["features"]:
            coords = data["features"][0]["geometry"]["coordinates"]
            full_address = data["features"][0]["place_name"]
            return coords[1], coords[0], full_address   # ✅ 3 values
    return None

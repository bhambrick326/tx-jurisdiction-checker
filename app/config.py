import os
from dotenv import load_dotenv

# Load variables from .env file (our lockbox of secrets)
load_dotenv()

# Mapbox settings
GEOCODER = os.getenv("GEOCODER", "mapbox")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN", "")

# File paths
CITY_LIMITS_PATH = os.getenv("CITY_LIMITS_PATH", "app/data/texas_city_limits.geojson")
PERMIT_LINKS_CSV = os.getenv("PERMIT_LINKS_CSV", "app/data/permit_links.csv")

# Security & Login
BASIC_AUTH_USER = os.getenv("BASIC_AUTH_USER", "")
BASIC_AUTH_PASS = os.getenv("BASIC_AUTH_PASS", "")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
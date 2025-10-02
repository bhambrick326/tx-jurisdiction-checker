from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

print("GEOCODER =", os.getenv("GEOCODER"))
print("MAPBOX_TOKEN =", os.getenv("MAPBOX_TOKEN"))
print("BASIC_AUTH_USER =", os.getenv("BASIC_AUTH_USER"))
print("BASIC_AUTH_PASS =", os.getenv("BASIC_AUTH_PASS"))
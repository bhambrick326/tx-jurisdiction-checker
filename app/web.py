from flask import Blueprint, render_template, request
from .geocode import geocode_address
from .jurisdiction import check_jurisdiction

web = Blueprint("web", __name__)

@web.route("/", methods=["GET", "POST"])
def index():
    result = None
    address = None   # default is None

    if request.method == "POST":
        address = request.form.get("address")
        if address:
            coords = geocode_address(address)
            if coords and len(coords) == 2:
                lat, lon = coords
                result = check_jurisdiction(lat, lon)
            else:
                result = {
                    "status": "error",
                    "city": None,
                    "permit_url": None,
                    "message": f"Geocoder returned unexpected data: {coords}"
                }

    # ✅ pass both result AND address to the template
    return render_template("index.html", result=result, address=address)

from flask import render_template, request
from .geocode import geocode_address
from .jurisdiction import check_jurisdiction

def init_web(app):
    # --- Routes ---
    @app.route("/", methods=["GET", "POST"])
    def index():
        result = None
        full_address = None

        if request.method == "POST":
            address = request.form.get("address")
            if address:
                coords = geocode_address(address)
                if coords:
                    # geocode.py returns (lat, lon, full_address)
                    lat, lon, full_address = coords
                    result = check_jurisdiction(lat, lon)

        return render_template("index.html", result=result, full_address=full_address)

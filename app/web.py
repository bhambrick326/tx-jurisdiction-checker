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
from flask import Flask, render_template, request, Response, redirect, url_for
import os
from functools import wraps

def create_app():
    app = Flask(__name__)

    # --- Authentication helpers ---
   def check_auth(username, password):
    return username == "admin" and password == "plumber123"

    def authenticate():
        return Response(
            "Login required", 401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'}
        )

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        return decorated

    @app.route("/")
    @requires_auth
    def index():
        return render_template("index.html")

    # --- Logout route ---
   @app.route("/logout")
def logout():
    """Force logout by sending a 401 Unauthorized"""
    return Response(
        "You have been logged out.", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )


    return app

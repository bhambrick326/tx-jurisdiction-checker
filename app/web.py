from flask import render_template, request, Response
from functools import wraps
from .geocode import geocode_address
from .jurisdiction import check_jurisdiction

def init_web(app):
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

    # --- Routes ---
    @app.route("/", methods=["GET", "POST"])
    @requires_auth
    def index():
        result = None
        if request.method == "POST":
            address = request.form.get("address")
            if address:
                coords = geocode_address(address)
                if coords:
                    lat, lon, full_address = coords
                    jurisdiction_result = check_jurisdiction(lat, lon)
                    result = f"{full_address} → {jurisdiction_result}"
                else:
                    result = "Could not geocode address"
        return render_template("index.html", result=result)

    # Optional logout route (still works if typed in URL)
    @app.route("/logout")
    def logout():
        return Response(
            "You have been logged out.", 401,
            {"WWW-Authenticate": 'Basic realm=\"Login Required\"'}
        )

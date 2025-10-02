from flask import Flask, render_template, request, Response
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

    @app.route("/logout")
    def logout():
        return Response(
            "You have been logged out.", 401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'}
        )

    return app

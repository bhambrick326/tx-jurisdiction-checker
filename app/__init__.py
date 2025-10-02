from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and initialize routes
    from .web import init_web
    init_web(app)

    return app

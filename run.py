from app import create_app   # <-- This should point to __init__.py, not web.py

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

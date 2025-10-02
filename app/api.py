from flask import Blueprint, request, jsonify
from .geocode import geocode_address
from .jurisdiction import check_jurisdiction

api = Blueprint("api", __name__)

@api.route("/jurisdiction/check", methods=["GET"])
def jurisdiction_check():
    """
    Example API endpoint:
    /api/jurisdiction/check?address=123+Main+St,+Houston,+TX
    """
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Missing address"}), 400

    coords = geocode_address(address)
    if not coords or len(coords) < 2:
        return jsonify({"error": "Could not geocode address"}), 400

    lat, lon, full_address = coords

    result = check_jurisdiction(lat, lon)
    result["full_address"] = full_address  # add for clarity

    return jsonify(result)

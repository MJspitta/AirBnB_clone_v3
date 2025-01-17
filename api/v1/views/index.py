#!/usr/bin/python3
"""create route /status on obj app_views"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """return json response for restfull api health"""
    resp = {"status": "OK"}
    return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """get number of each obj by type"""
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
    }
    return jsonify(stats)

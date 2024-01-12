#!/usr/bin/python3
"""
This is a script file that contains endpoint(route) status
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """
    This is a method that returns a JSON status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    This is a method that retrieves the number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")})

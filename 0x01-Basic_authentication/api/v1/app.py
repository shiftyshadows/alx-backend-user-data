#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from typing import Any, Tuple


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found_error(error: Any) -> Tuple[Any, int]:
    """
    Handles 404 Not Found errors.

    Args:
        error (Any): The error object captured by Flask.

    Returns:
        Tuple[Any, int]: JSON response and status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error: Any) -> Tuple[dict, int]:
    """
    Handles 401 Unauthorized errors.

    Args:
        error (Any): The error object captured by Flask.

    Returns:
        Tuple[dict, int]: JSON response and status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

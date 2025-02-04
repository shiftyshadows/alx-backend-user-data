#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from typing import Any, Tuple


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the auth variable
auth = None

if getenv("AUTH_TYPE") == "auth":
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request_handler():
    """
       Filters requests to secure the API based on authentication
       requirements.
    """
    # If no authentication instance, do nothing
    if auth is None:
        return

    # Define the list of paths that do not require authentication
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
    ]

    # Check if the path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Check for Authorization header
    if auth.authorization_header(request) is None:
        abort(401)

    # Check for a valid current user
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


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


@app.errorhandler(403)
def forbidden_error_handler(error: Exception) -> Tuple[dict, int]:
    """
    Error handler for 403 Forbidden HTTP status code.

    Purpose:
        Handles cases where a user is authenticated but lacks
        the necessary permissions to access a resource.

    Args:
        error (Exception): The HTTP exception that triggered the handler
            (e.g., from `abort(403)`).

    Returns:
        Tuple[dict, int]:
            - A dictionary containing the error message.
            - An HTTP status code of 403 (indicating Forbidden).
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

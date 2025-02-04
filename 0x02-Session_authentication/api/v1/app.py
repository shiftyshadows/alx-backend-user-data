#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.views import app_views  # ✅ Import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth  # ✅ Import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)  # ✅ Register app_views
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the auth variable
auth = None

AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    auth = SessionExpAuth()  # ✅ Use session authentication with expiration


@app.before_request
def before_request_handler():
    """
    Filters requests to secure the API based on authentication
    requirements.
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/',  # ✅ Exclude session login
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return  # Allow access

    if auth.authorization_header(request) is None and \
       auth.session_cookie(request) is None:
        abort(401)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)

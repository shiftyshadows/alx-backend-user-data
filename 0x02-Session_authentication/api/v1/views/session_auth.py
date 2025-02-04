#!/usr/bin/env python3
"""
Session Authentication View
"""
from flask import jsonify, request, make_response, abort
from models.user import User
from os import getenv
from api.v1.views import app_views  # ✅ Use app_views instead of Blueprint
from api.v1.auth.session_auth import SessionAuth

# ✅ Create local instance of SessionAuth
session_auth = SessionAuth()


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handles user login using session authentication.
    """
    if session_auth is None:
        abort(500)  # Ensure auth is initialized

    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # ✅ Create session and set cookie
    session_id = session_auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    session_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)

    return response

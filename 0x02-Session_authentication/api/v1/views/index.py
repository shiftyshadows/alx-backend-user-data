#!/usr/bin/env python3
""" Module of Index views
"""

from flask import jsonify, abort
from api.v1.views import app_views
from typing import NoReturn


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Return:
      - the number of each object
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized_access() -> None:
    """
    Endpoint that raises a 401 Unauthorized error.

    Raises:
        abort(401): Triggers the 401 error handler.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden_access() -> NoReturn:
    """
    Route to simulate or trigger a 403 Forbidden error.

    Purpose:
        This endpoint demonstrates or tests the behavior when
        a user is authenticated but does not have permission
        to access a resource.

    Endpoint:
        - Method: GET
        - URL: /api/v1/forbidden

    Behavior:
        Calls `abort(403)` to trigger the custom error handler
        for 403 Forbidden responses.

    Raises:
        HTTPException: A 403 Forbidden exception that is intercepted
            by the `@app.errorhandler(403)` in `api/v1/app.py`.
    """
    abort(403)

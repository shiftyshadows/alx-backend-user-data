#!/usr/bin/env python3
"""
   This module defines the class: Auth
"""
from typing import List, TypeVar
from flask import request
from os import getenv
# Create a generic User type for typing
User = TypeVar('User')


class Auth:
    """
    A class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (list): A list of paths that do not
            require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Ensure the path ends with a slash for consistency
        path = path if path.endswith('/') else f"{path}/"

        for excluded_path in excluded_paths:
            # Handle wildcard (*) at the end of an excluded path
            if excluded_path.endswith("*"):
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            else:
                if excluded_path.endswith('/'):
                    excluded_path = excluded_path
                else:
                    f"{excluded_path}/"
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from a request.

        Args:
            request (Request): The Flask request object.

        Returns:
            str: The Authorization header value if present, otherwise None.
        """
        if request is None:
            return None

        # Retrieve the Authorization header from the request
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from a request.

        Args:
            request (Request): The Flask request object.

        Returns:
            User: None for now, indicating no user management is implemented.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from the request.

        Args:
            request: Flask request object.

        Returns:
            str: The session ID stored in the cookie, or None if not found.
        """
        if request is None:
            return None

        # Get the session cookie name from environment variable
        session_name = getenv("SESSION_NAME")

        if session_name is None:
            return None

        # Return the session ID from the request cookies
        return request.cookies.get(session_name)

#!/usr/bin/env python3
"""
   This module defines the class: Auth
"""
from typing import List, TypeVar
from flask import request

# Create a generic User type for typing
User = TypeVar('User')


class Auth:
    """
    A class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not
            require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Normalize the path to ensure it ends with a slash for comparison
        path = path if path.endswith('/') else f"{path}/"

        # Check if the path is in the excluded paths
        for excluded_path in excluded_paths:
            if excluded_path == path:
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

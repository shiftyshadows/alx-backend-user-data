#!/usr/bin/env python3
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
            bool: False for now, indicating no authentication is required.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from a request.

        Args:
            request (Request): The Flask request object.

        Returns:
            str: None for now, indicating no authorization header is handled.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from a request.

        Args:
            request (Request): The Flask request object.

        Returns:
            User: None for now, indicating no user management is implemented.
        """
        return None

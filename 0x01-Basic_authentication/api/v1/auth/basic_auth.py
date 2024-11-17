#!/usr/bin/env python3
"""
   This module defines the class:BasicAuth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    For now, it is an empty implementation.
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The Authorization header
            string.

        Returns:
            str: The Base64 part of the Authorization header if
            valid, otherwise None.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Extract the part after "Basic " (index 6 onwards)
        return authorization_header[6:]

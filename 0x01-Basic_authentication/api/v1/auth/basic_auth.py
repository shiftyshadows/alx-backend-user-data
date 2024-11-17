#!/usr/bin/env python3
"""
   This module defines the class:BasicAuth
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User

UserType = TypeVar('User')


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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 string in the Authorization header.

        Args:
            base64_authorization_header (str): The Base64-encoded string.

        Returns:
            str: The decoded value as a UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string to bytes and convert to a UTF-8 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            # Return None if the Base64 string is invalid or decoding fails
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts the user email and password from the decoded Base64 string.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64
            string.

        Returns:
            (str, str): A tuple containing the user email and password, or
            (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        # Split the string into email and password at the first ':'
        user_email, password = decoded_base64_authorization_header.split(
            ":", 1
        )
        return user_email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
           Returns the User instance based on email and password.

           Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

           Returns:
            User: The User instance if valid, otherwise None.
        """
        # Validate input types
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        try:
            users = User.search({'email': user_email})
        except Exception:
            # Handle cases where User.search fails (e.g., DB errors)
            return None

        if not users or len(users) == 0:
            # No user linked to this email
            return None

        # Validate password for the first matched user
        user_instance = users[0]
        if not user_instance.is_valid_password(user_pwd):
            return None

        return user_instance

    def current_user(self, request=None) -> UserType:
        """
        Retrieves the User instance for a request.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance if authenticated, otherwise None.
        """
        # Get the Authorization header
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        # Extract Base64 part of the Authorization header
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        if not base64_auth_header:
            return None

        # Decode the Base64 string
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        if not decoded_auth_header:
            return None

        # Extract user credentials (email and password)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        if not user_email or not user_pwd:
            return None

        # Retrieve the User instance based on email and password
        return self.user_object_from_credentials(user_email, user_pwd)

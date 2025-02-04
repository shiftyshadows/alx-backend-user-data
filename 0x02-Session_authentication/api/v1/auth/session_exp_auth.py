#!/usr/bin/env python3
"""
Session Expiration Authentication module
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session authentication with expiration time """

    def __init__(self):
        """
        Initializes SessionExpAuth by setting the session duration.
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except ValueError:
            self.session_duration = 0  # Default to no expiration

    def create_session(self, user_id=None):
        """
        Creates a Session ID and stores session information.

        Args:
            user_id (str): The user ID to associate with the session.

        Returns:
            str: The generated session ID or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session details (user_id + creation time)
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves a User ID based on a given Session ID, checking expiration.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The associated User ID or None if session is expired or
            invalid.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        if "created_at" not in session_data:
            return None

        # Check if session is expired
        created_at = session_data["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None  # Session expired

        return session_data.get("user_id")

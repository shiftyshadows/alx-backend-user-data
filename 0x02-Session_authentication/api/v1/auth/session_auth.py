#!/usr/bin/env python3
"""
Session authentication module
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session-based authentication class """

    # Dictionary to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user_id.

        Args:
            user_id (str): The user ID to associate with the session.

        Returns:
            str: The generated session ID or None if invalid input.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        # Store session ID with associated user ID
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a User ID based on a given Session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The associated User ID or None if session_id is invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user_id associated with the session_id
        return self.user_id_by_session_id.get(session_id)

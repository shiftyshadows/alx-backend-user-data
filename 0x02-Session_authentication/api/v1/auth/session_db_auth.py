#!/usr/bin/env python3
"""
Session authentication with database (file) storage.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication using database storage. """

    def create_session(self, user_id=None):
        """
        Creates and stores a new UserSession instance.

        Args:
            user_id (str): The user ID to associate with the session.

        Returns:
            str: The generated session ID or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session in the "database"
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # ✅ Saves the session persistently

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves a User ID based on a session ID from the database.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The associated User ID or None if session is expired
            or not found.
        """
        if session_id is None:
            return None

        # Retrieve session from the database
        sessions = UserSession.search({"session_id": session_id})
        if not sessions or len(sessions) == 0:
            return None

        user_session = sessions[0]

        # Validate expiration using parent method
        return super().user_id_for_session_id(user_session.session_id)

    def destroy_session(self, request=None):
        """
        Deletes a user session (logs out) based on session ID from database.

        Args:
            request: Flask request object.

        Returns:
            bool: True if session was successfully deleted, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Retrieve session from database
        sessions = UserSession.search({"session_id": session_id})
        if not sessions or len(sessions) == 0:
            return False

        # Delete session from database
        for session in sessions:
            session.remove()

        return True  # ✅ Successfully deleted session

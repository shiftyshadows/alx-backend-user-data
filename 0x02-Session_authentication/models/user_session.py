#!/usr/bin/env python3
"""
UserSession model for database-based session storage.
"""
from models.base import Base


class UserSession(Base):
    """ Represents a User Session stored in a file/database. """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a UserSession instance.
        Attributes:
            user_id (str): The ID of the user.
            session_id (str): The session ID.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")

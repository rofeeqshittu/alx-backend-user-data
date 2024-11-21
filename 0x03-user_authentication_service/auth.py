#!/usr/bin/env python3
"""
Auth class for handling user authentication and session management
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance with a DB connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password."""
        try:
            # Check if user already exists
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # Hash the password and create new user
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's credentials."""
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            # No user found with that email
            return False
        return False

    def _hash_password(self, password: str) -> bytes:
        """Hashes the password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def _generate_uuid(self) -> str:
        """Generates a new UUID and returns it as a string."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a new session for the user and returns the session ID."""
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
            # Generate a new session ID (UUID)
            session_id = self._generate_uuid()
            # Store the session ID in the database
            user.session_id = session_id
            # Commit the change to the database
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            # Return None if no user is found
            return None

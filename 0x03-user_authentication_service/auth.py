#!/usr/bin/env python3
"""
Authentication module
"""
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance with a database instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user if they do not already exist.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user already exists with the provided email.
        """
        # Check if user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass  # User doesn't exist, continue

        # Hash the password
        hashed_password = _hash_password(password)

        # Add the user to the database
        user = self._db.add_user(email, hashed_password.decode('utf-8'))

        return user

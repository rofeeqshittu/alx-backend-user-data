#!/usr/bin/env python3
"""A module for authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a new UUID.

    Returns:
        str: A string representation of the new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    Provides methods for registering users, validating logins, managing
    sessions,
    and handling password resets.
    """

    def __init__(self):
        """Initializes a new Auth instance, connecting to the database.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new user to the database if the email doesn't already exist.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created user object.

        Raises:
            ValueError: If the user with the given email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
        except NoResultFound:
            # Add new user if email is not found
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.

        Args:
            email (str): The email of the user.
            password (str): The password entered by the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        user = None
        try:
            # Try to find the user by email
            user = self._db.find_user_by(email=email)
            if user is not None:
                # Check if the entered password matches the
                # hashed password in the database
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user and stores the session ID
        in the database.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID or None if the user is not found.
        """
        user = None
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        # Generate a session ID
        session_id = _generate_uuid()
        # Store the session ID in the database
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user based on a given session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User | None: The user object if found, otherwise None.
        """
        user = None
        if session_id is None:
            return None
        try:
            # Try to find the user by session ID
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session for a given user by setting the session ID
        to None.

        Args:
            user_id (int): The ID of the user whose session is to be destroyed.
        """
        if user_id is None:
            return None
        # Update the user to clear the session ID
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.

        Args:
            email (str): The email of the user requesting the reset.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If the user with the provided email doesn't exist.
        """
        user = None
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("User not found")
        # Generate a reset token and store it
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password given a valid reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password to set.

        Raises:
            ValueError: If the reset token is invalid or expired.
        """
        user = None
        try:
            # Find the user by reset token
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("Invalid reset token")
        # Hash the new password
        new_password_hash = _hash_password(password)
        # Update the password and clear the reset token
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )

#!/usr/bin/env python3
"""The `user` model's module.
This module defines the User class which represents the structure of a user
record in the database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Declare the base class for SQLAlchemy models
Base = declarative_base()


class User(Base):
    """Represents a record from the `user` table in the database.
    This class maps the attributes of a user to columns in the `users` table.
    """
    __tablename__ = "users"  # The name of the table in the database

    # The user ID (primary key) which uniquely identifies each user
    id = Column(Integer, primary_key=True)

    # The user's email, must be unique and cannot be null
    email = Column(String(250), nullable=False)

    # The hashed password of the user, stored securely
    hashed_password = Column(String(250), nullable=False)

    # The session ID associated with the user's current session
    session_id = Column(String(250), nullable=True)

    # The password reset token, used for resetting the user's password
    reset_token = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """String representation of a user.

        Returns:
            str: A human-readable string that represents the user.
        """
        return f"<User(id={self.id}, email={self.email}, session_id={
                self.session_id})>"

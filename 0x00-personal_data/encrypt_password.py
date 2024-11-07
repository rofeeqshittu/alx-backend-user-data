#!/usr/bin/env python3
"""
    Encrypt password module.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt, adding a salt for additional security.

    Args:
        password (str): The password to be hashed

    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

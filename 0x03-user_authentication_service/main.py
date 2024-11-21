#!/usr/bin/env python3
"""End-to-end integration test for the authentication service.
This module tests the user registration, login, profile, password reset, and logout features of the app.
"""
import requests

# Define constants for email, password, and new password
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test user registration by sending a POST request to /users endpoint.
    
    Args:
        email (str): User's email address.
        password (str): User's password.
    """
    response = requests.post(
        "http://localhost:5000/users",
        data={"email": email, "password": password},
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with a wrong password by sending a POST request to /sessions endpoint.
    
    Args:
        email (str): User's email address.
        password (str): Incorrect password.
    """
    response = requests.post(
        "http://localhost:5000/sessions",
        data={"email": email, "password": password},
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with correct credentials and return the session ID.
    
    Args:
        email (str): User's email address.
        password (str): User's password.
    
    Returns:
        str: The session ID for the logged-in user.
    """
    response = requests.post(
        "http://localhost:5000/sessions",
        data={"email": email, "password": password},
    )
    assert response.status_code == 200
    assert "session_id" in response.cookies
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Test accessing profile without being logged in by sending a GET request to /profile endpoint."""
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test accessing profile while logged in by sending a GET request to /profile endpoint.
    
    Args:
        session_id (str): The session ID for the logged-in user.
    """
    response = requests.get(
        "http://localhost:5000/profile", cookies={"session_id": session_id}
    )
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == EMAIL


def log_out(session_id: str) -> None:
    """Test logging out by sending a DELETE request to /sessions endpoint.
    
    Args:
        session_id (str): The session ID for the logged-in user.
    """
    response = requests.delete(
        "http://localhost:5000/sessions", cookies={"session_id": session_id}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def reset_password_token(email: str) -> str:
    """Test requesting a password reset token by sending a POST request to /reset_password endpoint.
    
    Args:
        email (str): User's email address.
    
    Returns:
        str: The reset token sent to the user's email.
    """
    response = requests.post(
        "http://localhost:5000/reset_password", data={"email": email}
    )
    assert response.status_code == 200
    assert "reset_token" in response.json()
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating the user's password by sending a PUT request to /reset_password endpoint.
    
    Args:
        email (str): User's email address.
        reset_token (str): The reset token for the user's password.
        new_password (str): The new password to be set.
    """
    response = requests.put(
        "http://localhost:5000/reset_password",
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    # Run the integration tests
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)


#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

# Initialize Flask app and Auth instance
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
        - The home page's payload.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Handles user registration.
    Expects 'email' and 'password' form data.
    If successful, creates a new user and returns a success message.
    If the email already exists, returns an error message.
    Return:
        - The account creation payload.
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        # Register the user
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        # Handle case where user already exists
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Handles user login.
    Expects 'email' and 'password' form data.
    If credentials are valid, creates a session and sets a cookie.
    If credentials are invalid, returns a 401 error.
    Return:
        - The account login payload.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        # Invalid login credentials
        abort(401)
    # Create session for the user
    session_id = AUTH.create_session(email)
    # Set the session ID as a cookie
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Handles user logout.
    Expects a session ID from the cookies.
    If valid, logs out the user by destroying the session.
    If the session is not found, returns a 403 error.
    Return:
        - Redirects to home route.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        # Invalid session
        abort(403)
    # Destroy the session
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Returns the user's profile information based on their session ID.
    If the user is not authenticated, returns a 403 error.
    Return:
        - The user's profile information.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        # No valid session
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Initiates the password reset process by sending a reset token to the user's email.
    If the email is valid, generates and returns a reset token.
    If the email is invalid, returns a 403 error.
    Return:
        - The user's password reset payload.
    """
    email = request.form.get("email")
    reset_token = None
    try:
        # Generate reset token for the user
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        reset_token = None
    if reset_token is None:
        # Invalid email
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Updates the user's password based on the provided reset token.
    Expects 'email', 'reset_token', and 'new_password' form data.
    If successful, updates the password and returns a success message.
    If the reset token is invalid, returns a 403 error.
    Return:
        - The user's password updated payload.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    is_password_changed = False
    try:
        # Update password
        AUTH.update_password(reset_token, new_password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False
    if not is_password_changed:
        # Failed to update password
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port="5000")

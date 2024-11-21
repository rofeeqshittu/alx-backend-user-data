#!/usr/bin/env python3
"""
Flask app to handle basic requests and user registration
"""

from flask import Flask, jsonify, request
from auth import Auth

# Initialize Flask app and Auth
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome_message():
    """
    Returns a welcome message in JSON format
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Registers a new user or returns an error if the user already exists.
    Expects 'email' and 'password' in the form data.
    """
    # Extract email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        # Attempt to register the user using the Auth class
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as err:
        # If user already exists, return error message
        return jsonify({"message": f"{err}"}), 400


if __name__ == "__main__":
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)

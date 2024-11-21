#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

# Add a user to test the 'update_user' method
email = 'test@test.com'
hashed_password = "hashedPwd"
user = my_db.add_user(email, hashed_password)
print(f"User ID: {user.id}")

# Update the user's password
try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

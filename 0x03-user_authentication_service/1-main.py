#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

# Add a user to test the 'find_user_by' method
user = my_db.add_user("test@test.com", "PwdHashed")
print(f"User ID: {user.id}")

# Find the user by email
find_user = my_db.find_user_by(email="test@test.com")
print(f"Found User ID: {find_user.id}")

# Test case where user is not found
try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(f"Found User ID: {find_user.id}")
except NoResultFound:
    print("Not found")

# Test case where an invalid query is made
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(f"Found User ID: {find_user.id}")
except InvalidRequestError:
    print("Invalid")

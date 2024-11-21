#!/usr/bin/env python3
"""
Main file to test the User model.
"""
from user import User

print(User.__tablename__)  # Should print: users

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

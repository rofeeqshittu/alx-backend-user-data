#!/usr/bin/env python3
"""
Main file
"""
from db import DB

my_db = DB()

# Add the first user
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(f"User 1 ID: {user_1.id}")

# Add the second user
user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(f"User 2 ID: {user_2.id}")

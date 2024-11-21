# User Authentication Service

## Overview

This project involves implementing a user authentication service using Python, Flask, SQLAlchemy, and bcrypt. The service includes features such as user registration, secure password hashing, session management, and more. 

The application is designed to simulate a full-fledged user authentication backend, complete with database integration, password security, and session handling.

![User-authentication-service](user-auth-service.jpg)

## Concepts

The following concepts are covered in this project:

- Database modeling with SQLAlchemy
- Secure password hashing using `bcrypt`
- Flask-based API development
- HTTP authentication techniques
- Session management and UUID generation
- Error handling in APIs

## Tasks

| Task Number | Filename | Description |
|-------------|----------|-------------|
| 0 | [user.py](./user.py) | Define the SQLAlchemy `User` model for the `users` table with attributes like `id`, `email`, `hashed_password`, `session_id`, and `reset_token`. |
| 1 | [db.py](./db.py) | Implement the `add_user` method in the `DB` class to add new users to the database. |
| 2 | [db.py](./db.py) | Implement the `find_user_by` method to retrieve a user using keyword arguments and handle exceptions appropriately. |
| 3 | [db.py](./db.py) | Implement the `update_user` method to update a user's attributes in the database and handle invalid attribute updates. |
| 4 | [auth.py](./auth.py) | Define the `_hash_password` method to securely hash passwords using `bcrypt`. |
| 5 | [auth.py](./auth.py) | Implement the `register_user` method in the `Auth` class to register a new user while ensuring unique email constraints. |
| 6 | [app.py](./app.py) | Set up a basic Flask app with a GET route at `/` to return a welcome message. |
| 7 | [app.py](./app.py) | Implement the POST `/users` route to register a user, handle duplicates, and return appropriate JSON responses. |
| 8 | [auth.py](./auth.py) | Implement the `valid_login` method to validate user credentials using `bcrypt.checkpw`. |
| 9 | [auth.py](./auth.py) | Implement a `_generate_uuid` method to generate a UUID string for session handling. |
| 10 | [auth.py](./auth.py) | Implement the `create_session` method to associate a UUID session ID with a user in the database. |
| 11 | [app.py](./app.py) | Implement the POST `/sessions` route to log in a user and set a session ID cookie. |
| 12 | [auth.py](./auth.py) | Implement the `get_user_from_session_id` method to retrieve a user from a session ID. |
| 13 | [auth.py](./auth.py) | Implement the `destroy_session` method to log out a user by invalidating their session ID. |
| 14 | [app.py](./app.py) | Implement the DELETE `/sessions` route to log out a user by clearing their session ID. |

## Setup Environment

1. **Operating System**: Ubuntu 18.04 LTS  
2. **Python Version**: Python 3.7  
3. **Database**: SQLite  
4. **Dependencies**:  
   - `Flask`
   - `SQLAlchemy`
   - `bcrypt`
   - `uuid`

### Steps to Set Up the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/rofeeqshittu/alx-backend-user-data.git
   cd alx-backend-user-data/0x03-user_authentication_service
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:
    ```bash
    python3 app.py
    ```

4. Test the endpoints using `curl` or an API client like Postman.
---

## Resources
- [Flask documentation](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Requests module](https://requests.kennethreitz.org/en/latest/user/quickstart/)
- [HTTP status codes](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
- [Mapping declaration](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping)

# Session Authentication Project

## Overview

In this project, we implement a Session Authentication system to manage user login and logout processes securely. For educational purposes, we are building the session management from scratch rather than using libraries (e.g., `Flask-HTTPAuth`), to gain a deeper understanding of session-based authentication.

---

## Concepts

1. **Session Authentication**: Method of managing user sessions through session IDs stored in cookies.
2. **HTTP Cookies**: Small pieces of data sent by the server to store user session details on the client side.
3. **Flask**: Micro web framework for Python, used for handling web routes, requests, and responses.

---

## Project Structure

The project consists of multiple files that manage different aspects of session authentication. We utilize existing work from the previous Basic Authentication project, expanding upon it to support session-based authentication.

---

## Tasks

| Task No | Filename                                | Description                                                                                             |
|---------|-----------------------------------------|---------------------------------------------------------------------------------------------------------|
| 0       | [Et moi et moi et moi!](./api/v1/app.py)            | Add endpoint `/users/me` to retrieve the authenticated User object.                                     |
| 1       | [Empty session](./api/v1/auth/session_auth.py)       | Create a class `SessionAuth` that inherits `Auth` as a placeholder for session management.               |
| 2       | [Create a session](./api/v1/auth/session_auth.py)    | Implement `create_session` to generate and store Session IDs for user sessions.                          |
| 3       | [User ID for Session ID](./api/v1/auth/session_auth.py) | Implement `user_id_for_session_id` to retrieve User IDs based on Session IDs.                          |
| 4       | [Session cookie](./api/v1/auth/auth.py)              | Add `session_cookie` method to retrieve the session cookie from requests.                               |
| 5       | [Before request](./api/v1/app.py)                    | Update `@app.before_request` to check for valid session or authorization headers.                       |
| 6       | [Use Session ID for identifying a User](./api/v1/auth/session_auth.py) | Implement `current_user` method to return the User instance based on session ID.                      |
| 7       | [New view for Session Authentication](./api/v1/views/session_auth.py) | Add a POST route to handle user login with session authentication.                                      |
| 8       | [Logout](./api/v1/views/session_auth.py)                | Add a DELETE route to handle user logout by deleting the session ID cookie.                             |
| 9       | [Expiration](./api/v1/auth/session_exp_auth.py) | Add session expiration functionality to manage session duration and timeouts.                                 |
| 10      | [Sessions in Database](./api/v1/auth/session_db_auth.py) | Store session information in a persistent file-backed database.                                        |

---
---

### Task Details

#### 0. Et moi et moi et moi!

**Filename**: `api/v1/app.py`

**Objective**: Add a new endpoint, `GET /users/me`, to retrieve the authenticated User object.
- Copy files from the previous Basic Authentication project.
- Update `@app.before_request` in `api/v1/app.py` to assign the result of `auth.current_user(request)` to `request.current_user`.
- Modify `GET /api/v1/users/<user_id>` to handle cases where `<user_id>` is `"me"`.

---

#### 1. Empty session

**Filename**: `api/v1/auth/session_auth.py`

**Objective**: Create an empty class `SessionAuth` that inherits from `Auth`.
- Verify correct inheritance without overloading and validate switching based on environment variables.

---

#### 2. Create a session

**Filename**: `api/v1/auth/session_auth.py`

**Objective**: Implement `create_session` to generate and store Session IDs for user sessions.
- Create `user_id_by_session_id`, a dictionary to store `user_id` by `session_id`.
- Use `uuid4()` from the `uuid` module to generate unique Session IDs.

---

#### 3. User ID for Session ID

**Filename**: `api/v1/auth/session_auth.py`

**Objective**: Implement `user_id_for_session_id` to retrieve User IDs based on Session IDs.
- Return `None` if the session ID is invalid or does not exist in `user_id_by_session_id`.

---

#### 4. Session cookie

**Filename**: `api/v1/auth/auth.py`

**Objective**: Add `session_cookie` method to retrieve the session cookie from requests.
- Check for `_my_session_id` as defined by the environment variable `SESSION_NAME`.

---

#### 5. Before request

**Filename**: `api/v1/app.py`

**Objective**: Update `@app.before_request` to enforce session or authorization headers.
- Add `/api/v1/auth_session/login/` to excluded paths.
- If both `auth.authorization_header(request)` and `auth.session_cookie(request)` are `None`, return `401 Unauthorized`.

---

#### 6. Use Session ID for identifying a User

**Filename**: `api/v1/auth/session_auth.py`

**Objective**: Implement `current_user` method to return the User instance based on session ID.
- Use `session_cookie` to get the User ID from the session ID.
- Retrieve the User instance using `User.get(user_id)`.

---

#### 7. New view for Session Authentication

**Filename**: `api/v1/views/session_auth.py`

**Objective**: Create a POST route to manage login sessions.

- **Route**: `POST /auth_session/login` (also accessible at `/api/v1/auth_session/login`).
- **Requirements**:
  - Slash tolerant.
  - Retrieve `email` and `password` parameters using `request.form.get()`.
  - Validations:
    - Return `{ "error": "email missing" }` with `400` if `email` is missing or empty.
    - Return `{ "error": "password missing" }` with `400` if `password` is missing or empty.
    - Retrieve `User` based on `email` using `User.search(...)`.
    - If no `User` is found, return `{ "error": "no user found for this email" }` with `404`.
    - If password is incorrect, return `{ "error": "wrong password" }` with `401` using `is_valid_password`.
  - If successful:
    - Use `auth.create_session(user_id)` to create a session.
    - Return the user's details with session ID in a cookie named `_my_session_id`.

**Example**:
```bash
curl -X POST "http://0.0.0.0:5000/api/v1/auth_session/login" -d "email=user@example.com" -d "password=correct_password"
# Returns JSON with User info and sets the session cookie
```

---

#### 8. Logout
Filename: `api/v1/views/session_auth.py`

Objective: Create a DELETE route to handle user logout by destroying the session ID cookie.

Requirements:
- Update `SessionAuth` class:
- Add `destroy_session(self, request=None).`
    - Returns `False` if `request` is `None` or the session cookie is missing.
    - Returns `False` if the session cookie is not linked to any `User ID`.
    - Deletes the session from user_id_by_session_id and returns True.
- Route: DELETE /auth_session/logout (slash tolerant).
- If `destroy_session` returns `False`, return `404`.

**Example**
```bash
curl -X DELETE "http://0.0.0.0:5000/api/v1/auth_session/logout" -H "Cookie: _my_session_id=session_id_value"
# Logs the user out by removing their session
```

---

#### 9. Expiration

**Filename**: `api/v1/auth/session_exp_auth.py`

**Objective**: Add session expiration to the authentication system by inheriting from `SessionAuth`.
- Create a `SessionExpAuth` class inheriting `SessionAuth`.
- **`__init__` Method**:
  - Add `session_duration` from environment variable `SESSION_DURATION`, casting it to an integer. If not present or invalid, set `session_duration` to `0` (unlimited session).
- **`create_session` Method**:
  - Call `super()` to create a Session ID.
  - Store the session data as a dictionary with `user_id` and `created_at` (current datetime) in `user_id_by_session_id`.
- **`user_id_for_session_id` Method**:
  - Return `user_id` if `session_duration` is `0` (unlimited).
  - Return `None` if `created_at` is missing or the session has expired.
  - Otherwise, return `user_id`.

**Example Usage**:

```bash
# Run the server with session expiration set to 60 seconds
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_exp_auth SESSION_NAME=_my_session_id SESSION_DURATION=60 python3 -m api.v1.app
Login with session authentication:
```bash
curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d "email=user@example.com" -d "password=correct_password"
Access /users/me after a few seconds to see active session and after 60 seconds to confirm timeout.
```

---

#### 10. Sessions in Database
Filename: `api/v1/auth/session_db_auth.py`

Objective: Store session data in a persistent file-based database so session data is retained if the server restarts.

UserSession Model: Define models/user_session.py to inherit Base with attributes:
user_id: Unique identifier for the user.
session_id: Unique identifier for the session.
SessionDBAuth Class:
Inherit SessionExpAuth.
create_session:
Calls super() to create a Session ID.
Stores each session as a new instance of UserSession saved in the file database.
user_id_for_session_id:
Retrieves User ID by querying the UserSession instances stored in the database.
destroy_session:
Deletes the UserSession instance for a given session ID.
Example Usage:

```bash
# Start server with database-backed session
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_db_auth SESSION_NAME=_my_session_id SESSION_DURATION=60 python3 -m api.v1.app
```
---
---

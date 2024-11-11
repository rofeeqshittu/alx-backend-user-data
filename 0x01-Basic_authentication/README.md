# 0x01. Basic Authentication

## Overview
This project introduces the concept of Basic Authentication, a method of securing an API using encoded credentials. It covers how to implement a simple authentication mechanism and handle unauthorized and forbidden access. By the end of this project, you'll understand how authentication headers work, how to decode Base64 strings, and how to manage secure API requests.

![Authentication failed, you shall not pass](authentication-failed.png)

## About
Basic Authentication is an essential part of web security. This project demonstrates a simple approach to secure an API by encoding and decoding credentials and handling HTTP status codes for unauthorized and forbidden requests.

## Concepts
- Basic Authentication
- Base64 encoding/decoding
- HTTP Authorization headers
- Flask API error handling

## Tasks

| Task No. | Filename                                    | Description                                                                                                                                                                                                                              |
|----------|---------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0        | [api/v1/app.py](api/v1/app.py)              | Initializes the basic API setup.                                                                                                                                                                                                         |
| 1        | [api/v1/views/index.py](api/v1/views/index.py) | Adds error handling for unauthorized requests (401 status code).                                                                                                                                                                         |
| 2        | [api/v1/views/index.py](api/v1/views/index.py) | Adds error handling for forbidden requests (403 status code).                                                                                                                                                                            |
| 3        | [api/v1/auth/auth.py](api/v1/auth/auth.py)  | Defines the Auth class to manage the API authentication process.                                                                                                                                                                         |
| 4        | [api/v1/auth/auth.py](api/v1/auth/auth.py)  | Updates the `require_auth` method to define unauthenticated routes.                                                                                                                                                                      |
| 5        | [api/v1/app.py](api/v1/app.py)              | Implements request validation and secure handling of API requests with authorization header validation.                                                                                                                                  |
| 6        | [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) | Creates BasicAuth class to handle basic authentication based on the environment variable `AUTH_TYPE`.                                                                                                                                    |
| 7        | [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) | Implements method `extract_base64_authorization_header` to extract the Base64 encoded part of the Authorization header.                                                                                                                  |
| 8        | [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) | Implements method `decode_base64_authorization_header` to decode the Base64 string into readable credentials.                                                                                                                            |

## Setup
To set up the API locally:

```bash
$ pip3 install -r requirements.txt
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app


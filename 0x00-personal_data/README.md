# 0x00. Personal Data

## Overview
This project focuses on handling Personally Identifiable Information (PII) in a secure and compliant way. By implementing filters, encryption, and database authentication, you will gain experience in protecting sensitive data and managing log files. This project emphasizes responsible logging practices and secure access management using environment variables.

![I don't always post info about myself....](i-dont-post-info-about-myself-but-when.png)

## Concepts
- **Personally Identifiable Information (PII)**: Understanding and managing sensitive data such as names, email addresses, and social security numbers.
- **Log Filtering**: Obfuscating sensitive fields within log messages to ensure data security.
- **Password Encryption**: Implementing encryption for secure password storage and validation.
- **Database Authentication**: Connecting securely to a database using environment variables.

## Tasks

| Task No | Filename                  | Description                                                                                                  |
|---------|----------------------------|--------------------------------------------------------------------------------------------------------------|
| 0       | [filtered_logger.py](./filtered_logger.py) | Write a function `filter_datum` to obfuscate specific fields in log messages using regex substitution.       |
| 1       | [filtered_logger.py](./filtered_logger.py) | Implement `RedactingFormatter` class to filter out PII fields from logs based on the specified format.      |
| 2       | [filtered_logger.py](./filtered_logger.py) | Create a `get_logger` function that sets up logging for user data with an appropriate log level and format. |
| 3       | [filtered_logger.py](./filtered_logger.py) | Implement `get_db` to connect securely to a database using environment variables for credentials.           |
| 4       | [filtered_logger.py](./filtered_logger.py) | Create a `main` function to read and display filtered data from the `users` table using `get_db`.           |

## Files and Descriptions

### [filtered_logger.py](./filtered_logger.py)
Handles various functions related to data filtering, logging, and database connection:
- **filter_datum**: Obfuscates specified fields in log messages.
- **RedactingFormatter**: Custom log formatter to filter PII fields.
- **get_logger**: Configures a logger for managing user data logging with secure formatting.
- **get_db**: Establishes a secure database connection using credentials stored in environment variables.
- **main**: Reads all rows from the `users` table, applying field filtering before output.

## Setup Environment
- **Operating System**: Ubuntu 18.04 LTS
- **Python Version**: 3.7
- **MySQL Version**: MySQL 5.7
- **Packages**: Install required packages using:
  ```bash
  pip3 install mysql-connector-python bcrypt

Ensure you have the following environment variables set for database access:

- `PERSONAL_DATA_DB_USERNAME` (default: "root")
- `PERSONAL_DATA_DB_PASSWORD` (default: "")
- `PERSONAL_DATA_DB_HOST` (default: "localhost")
- `PERSONAL_DATA_DB_NAME` (database name)

Run the module directly to execute the main function:
```bash
PERSONAL_DATA_DB_USERNAME=<username> PERSONAL_DATA_DB_PASSWORD=<password> PERSONAL_DATA_DB_HOST=<host> PERSONAL_DATA_DB_NAME=<dbname> ./filtered_logger.py
```

---

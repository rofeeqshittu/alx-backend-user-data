#!/usr/bin/env python3
"""
    This module provide a function to obfuscate specified fields
    in log messages.
"""
import logging
import re
import os
import mysql.connector
from datetime import datetime
from typing import List


# Define the fields considered as PII
PII_FIELDS = ("email", "ssn", "password", "phone", "address")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates the value of specified fields in a log message.
    """
    pattern = f'({"|".join(fields)})=[^{separator}"]+'
    return re.sub(pattern, lambda x: f'{x.group(1)}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize RedactingFormatter with fields to be obfuscated."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record, obfuscating specified fields. """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger object with RedactingFormatter.
    The logger is name 'user_data' and will log messages up to INFO level.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)  # Set log level to INFO
    logger.propagate = False  # Prevent propagation to other loggers

    # Create a stream handler for logging to console
    stream_handler = logging.StreamHandler()

    # Create a formatter and apply RedactingFormatter with PII_FIELDS
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


# Setting up logging format
logging.basicConfig(
        format='[HOLBERTON] user_data INFO %(asctime)s,000: %(message)s',
        level=logging.INFO
        )

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish a connection to the MySQL database using credentials from
    environment variables.
    Returns a MySQL connection object.
    """
    # Retrieve credentials from environment variables, with default values
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    if not db_name:
        raise ValueError("Database name (PERSONAL_DATA_DB_NAME) is required.")

    # Connect to the database using the credentials
    db_connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
            )
    return db_connection

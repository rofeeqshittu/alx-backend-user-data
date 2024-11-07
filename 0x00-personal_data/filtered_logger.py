#!/usr/bin/env python3
"""
    This module provide a function to obfuscate specified fields
    in log messages.
"""
import logging
import re
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

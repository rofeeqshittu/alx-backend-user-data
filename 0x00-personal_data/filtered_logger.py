#!/usr/bin/env python3
"""
    This module provide a function to obfuscate specified fields
    in log messages.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates the value of specified fields in a log message.
    """
    pattern = f'({"|".join(fields)})=[^{separator}"]+'
    return re.sub(pattern, lambda x: f'{x.group(1)}={redaction}', message)

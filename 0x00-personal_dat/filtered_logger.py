#!/usr/bin/env python3
"""
Regex-ing
"""
import re
import os
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        format function
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    filter_datum function
        # . -> match a character
        # + -> match more than one
        # ? -> repeat the next text of the match
    """
    for field in fields:
        message = re.sub(fr'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    get_logger function
    source: https://realpython.com/python-logging/
    """
    # name of the logger
    logger = logging.getLogger("user_data")
    # set level to INFO
    logger.setLevel(logging.INFO)
    # propagate message
    logger.propagate = False
    # create the handle
    c_handler = logging.StreamHandler()
    # change format
    c_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # add handler
    logger.addHandler(c_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db function
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )


def main():
    """
    main function
    """
    conn = get_db()
    users = conn.cursor()
    users.execute("SELECT CONCAT('name=', name, ';ssn=', ssn, ';ip=', ip, \
        ';user_agent', user_agent, ';') AS message FROM users;")
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger()

    for user in users:
        logger.log(logging.INFO, user[0])


if __name__ == "__main__":
    main()

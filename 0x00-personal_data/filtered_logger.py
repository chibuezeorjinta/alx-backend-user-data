#!/usr/bin/env python3
"""filter using logger"""
import logging
import re
import mysql.connector
from typing import List
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate a string"""
    for field in fields:
        message = re.sub(r'(?<={}=).+?(?={})'.format(field,
                         separator), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """Run the formatter in a logger format"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger():
    """create a logger"""
    logger = logging.getLogger('user_data')
    # set level
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # create stream handler
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connect to a mysql server securely"""
    connection_db = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME'))

    return connection_db


def main():
    """Main function. to get a logger and connect to database"""
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    log = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(str_row.strip())

    cursor.close()
    database.close()


if __name__ == '__main__':
    main()

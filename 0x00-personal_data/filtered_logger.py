#!/usr/bin/env python3
"""filter using logger"""
import logging
import os
import re
from mysql import connector
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple, Union, NoReturn

PII_FIELDS: Tuple[str, str, str, str, str] = (
    'name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate the provided [fields] in the string[message] with
    the provided [redaction] using [seperator] as a marker.
    :param fields: list[str] = parts of the message to
                                                            obfuscate.
    :param redaction: [str] = replacement characters.
    :param message: str = provide string to obfuscate
    :param separator: str = seperator character as a guide.
    :return: str = obfuscated string.
    """
    for field in fields:
        message = re.sub(r'(?<={}=).+?(?={})'.format(
            field, separator), redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
     Redacting Formatter class.
     used in creating a logger for the user.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """
        Class constructor.
        :param fields: list[str] = list of fields that are
                                    expected to be obfuscated. None by default.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Reformat a given string[record] into a log. Obfuscating
        fields as needed.
        :param record: str = A given string record.
        :return: str = reformatted string.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Create a logger object according to specifications.
    :return: logging.logger
    """
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


def get_db() -> Union[MySQLConnection, None]:
    """
    Log into a mysql server securely.
    :return: A Mysql connection object or None.
                    if it fails.
    """
    # Get database credentials from environment variables with default values
    db_username: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name: str = os.getenv("PERSONAL_DATA_DB_NAME")

    try:
        # Connect to the database
        connection: MySQLConnection = connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return connection
    except connector.Error as err:
        print("Error connecting to the database:", err)
        return None


def main() -> NoReturn:
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

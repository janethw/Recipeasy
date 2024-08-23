import mysql.connector
from mysql.connector import Error
from config import USER, PASSWORD, HOST, DB_NAME
from logging_utils import init_logger, logger_message

_logger = init_logger()


# custom exceptions for handling database connection and retrieval errors
class ExceptionDatabaseConnectionFailed(Exception):
    pass


class DataNotFound(Exception):
    pass


# class to handle db management
class SQLDatabase:
    def __init__(self):
        self._host = HOST
        self._database = DB_NAME
        self._user = USER
        self._password = PASSWORD
        self._conn = None

    # establish a db connection
    def connect(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='connect', message='entry'))
        try:
            self._conn = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database)
            if self._conn.is_connected():
                _logger.debug(logger_message.format(module_name=__name__, function_name='connect',
                                                    message='Connected to MySQL database'))
        except Error as e:
            _logger.critical(logger_message.format(module_name=__name__, function_name='connect',
                                                   message=f'Failed to connect to database: {e}'))
            self._conn = None
            raise ExceptionDatabaseConnectionFailed(e)

    # execute a MySQL query
    def _execute_query(self, query, params=None, fetch_one=False):
        _logger.debug(logger_message.format(module_name=__name__, function_name='_execute_query', message='entry'))
        if self._conn is None:
            self.connect()
        if self._conn is not None:
            # automatically close cursor when finished
            with self._conn.cursor() as cursor:
                try:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                except Error as e:
                    _logger.error(logger_message.format(module_name=__name__, function_name='_execute_query',
                                                        message=f'Unable to execute query: {e}'))
                    raise e
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        return None

    def query_data(self, query, parameters=None):
        _logger.debug(logger_message.format(module_name=__name__, function_name='query_data', message='entry'))
        return self._execute_query(query, parameters)

    def insert_update_data(self, query, parameters, commit=True):
        _logger.debug(logger_message.format(module_name=__name__, function_name='insert_update_data', message='entry'))
        self._execute_query(query, parameters)
        if commit:
            self._conn.commit()

    def commit(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='commit', message='entry'))
        self._conn.commit()

    def rollback(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='rollback', message='entry'))
        self._conn.rollback()

    def close(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='close', message='entry'))
        if self._conn is not None and self._conn.is_connected():
            self._conn.close()
            _logger.debug(logger_message.format(module_name=__name__, function_name='close',
                                                message='Database connection closed'))

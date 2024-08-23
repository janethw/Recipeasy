from db_utils import SQLDatabase
from logging_utils import init_logger
from mysql.connector import Error

_logger = init_logger()  # initialising the logger but not at class


class LoginSQLDatabase(SQLDatabase):

    def register(self, username, email, password_hash):
        query = ("INSERT INTO user_login (username, email, password_hash) "
                 "VALUES(%s, %s, %s)")
        params = (username, email, password_hash)
        try:
            self._execute_query(query, params)
            self.commit()
        except Error:
            raise ValueError('Username Taken')

    def get(self, username):
        query = ("SELECT password_hash, email "
                 "FROM user_login "
                 "WHERE username = %s")
        params = (username, )
        try:
            response = self._execute_query(query, params, fetch_one=True)
            if response:
                print(f'in get method in db_utils, response is: {response}')
                # returns the stored password hash
                return response
            else:
                # Handle case where user logs on with incorrect details
                print('No data found for given query. Returning None.')
                return None
        except Error as e:
            print(f'Error: {e}')

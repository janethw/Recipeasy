# Flask global object g used for temporary storage for each request, used here to manage database connection
from flask import g
from login.login_files.login_db_utils import LoginSQLDatabase


class LoginDatabaseConnectionHandler:
    @staticmethod
    def get_db():
        # check if there is already a db connection stored in g
        if 'login_db' not in g:
            g.login_db = LoginSQLDatabase()
            g.login_db.connect()
        return g.login_db

    @staticmethod
    def close_db():
        # remove db from g to close the connection
        db = g.pop('login_db', None)
        if db is not None:
            db.close()

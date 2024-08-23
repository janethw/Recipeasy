
from flask import session, redirect, url_for
from functools import wraps
from quiz.quiz_files.quiz_app_utils import QuizDatabaseConnectionHandler
from login.login_files.login_app_utils import LoginDatabaseConnectionHandler


# class handling database connection operations
class DatabaseConnectionHandler:
    # get the database connection
    @staticmethod
    def get_db():
        QuizDatabaseConnectionHandler.get_db()
        LoginDatabaseConnectionHandler.get_db()

    # close the database connection
    @staticmethod
    def close_db():
        QuizDatabaseConnectionHandler.close_db()
        LoginDatabaseConnectionHandler.close_db()


# decorator function to check if a user is logged in
def login_required(f):
    @wraps(f)
    def wrapper_func(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))  # replace 'login' with your login route
        return f(*args, **kwargs)
    return wrapper_func



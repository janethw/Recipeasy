# Flask global object g used for temporary storage for each request, used here to manage database connection
from flask import g
from quiz.quiz_files.quiz_db_utils import QuizSQLDatabase


class QuizDatabaseConnectionHandler:
    @staticmethod
    def get_db():
        # check if there is already a db connection stored in g, create one if required
        if 'quiz_db' not in g:
            g.quiz_db = QuizSQLDatabase()
            g.quiz_db.connect()
        return g.quiz_db

    @staticmethod
    def close_db():
        # remove db from g to close the connection
        db = g.pop('quiz_db', None)
        if db is not None:
            db.close()

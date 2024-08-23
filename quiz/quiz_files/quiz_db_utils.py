from db_utils import SQLDatabase
from logging_utils import init_logger
from mysql.connector import Error

_logger = init_logger()  # initialising the logger but not at class


class QuizSQLDatabase(SQLDatabase):

    def fetch_correct_answer(self, correct_answer_id):
        query = ("SELECT choice_text "
                 "FROM answers AS a "
                 "INNER JOIN questions AS q "
                 "ON q.correct_answer_id = a.choice_id "
                 "WHERE q.correct_answer_id = %s "
                 "LIMIT 1")
        params = (correct_answer_id, )
        response = self._execute_query(query, params)
        return response

    def get_question(self, question_id):
        query = ("SELECT question_id, question_text, correct_answer_id, difficulty "
                 "FROM questions "
                 "WHERE question_id = %s "
                 "LIMIT 1")
        params = (question_id,)
        try:
            response = self._execute_query(query, params)
            if response:
                return response
            else:
                print('No data found for given query. Returning None.')
                return None
        except Error as e:
            print(f'Error: {e}')
            return None

    def get_question_answers(self, question_id):
        query = ("SELECT choice_text "
                 "FROM answers "
                 "WHERE question_id = %s "
                 "LIMIT 4")
        params = (question_id,)
        try:
            response = self._execute_query(query, params)
            if response:
                # assuming 4 answers per question
                return response
            else:
                print('No data found for given query. Returning None.')
                return None
        except Error as e:
            print(f'Error: {e}')
            return None

    def get_answers(self):
        query = ("SELECT choice_text "
                 "FROM answers ")
        try:
            response = self._execute_query(query)
            if response:
                return response
            else:
                print('No data found for given query. Returning None.')
                return None
        except Error as e:
            print(f'Error: {e}')
            return None

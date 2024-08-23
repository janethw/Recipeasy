from flask import render_template, session
import random
import requests
from app_utils import login_required


class QuizModule:
    # QuizModule class constructor
    def __init__(self):
        self.question = None
        self.answer1 = None
        self.answer2 = None
        self.answer3 = None
        self.answer4 = None

    # class method called by main.py and creates a new instance of QuizModule
    @classmethod
    @login_required
    def start(cls):
        quiz = cls()
        # start the quiz by getting the questions from the db
        quiz.start_quiz()
        # render the quiz homepage template with first question and answer choices
        return quiz.quiz_homepage()

    @staticmethod
    def initialise_session_for_quiz():
        session['user_score'] = 0
        session['list_of_asked_questions_by_id'] = []
        session['question_id'] = None
        session['correct_answer_id'] = None

    @staticmethod
    def get_question_id():
        while True:
            # randomly generate question_id to add interest
            question_id = random.randint(1, 30)
            if question_id not in session['list_of_asked_questions_by_id']:
                session['list_of_asked_questions_by_id'].append(question_id)
                # exit while loop once an unused question_id has been generated
                break
        return question_id

    def start_quiz(self):
        # set Flask session variables for score and list_of_asked_questions_by_id
        self.initialise_session_for_quiz()
        self.generate_quiz()

    def generate_quiz(self):
        try:
            session['question_id'] = self.get_question_id()
            self.get_question()
            self.get_question_answers()
        except Exception as e:
            print('Error in generate_quiz', str(e))
            raise

    def quiz_homepage(self):
        # render template based on randomly selected question
        return render_template('quiz.html',
                               session_quiz_number=len(session['list_of_asked_questions_by_id']),
                               correct_answer_id=session['correct_answer_id'],
                               user_score=session['user_score'],
                               question=self.question,
                               answer1=self.answer1,
                               answer2=self.answer2,
                               answer3=self.answer3,
                               answer4=self.answer4)

    def get_question(self):
        question_id = session['question_id']

        # pass random_number to the route as a parameter to find the corresponding question_id
        response = requests.get(
            f'http://127.0.0.1:5000/quiz/get_question/{question_id}',
            headers={'content-type': 'application/json'}
        )

        # parse JSON response if successful status code
        if response.status_code == 200:
            try:
                question_row_from_db = response.json()['question']
                self.question = question_row_from_db[0][1]
                correct_answer_id = question_row_from_db[0][2]
                session['correct_answer_id'] = correct_answer_id
            except Exception:
                raise

    def get_question_answers(self):
        response = requests.get(
            f'http://127.0.0.1:5000/quiz/get_question_answers/{session["question_id"]}',
            headers={'content-type': 'application/json'}
        )

        # parse JSON response if successful status code
        if response.status_code == 200:
            try:
                question_answers_from_db = response.json()['question_answers']
                self.answer1 = question_answers_from_db[0][0]
                self.answer2 = question_answers_from_db[1][0]
                self.answer3 = question_answers_from_db[2][0]
                self.answer4 = question_answers_from_db[3][0]
            except Exception:
                print(f'An error occurred while getting question: {response.status_code}')
                raise

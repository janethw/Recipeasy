import itertools
from flask import jsonify, render_template, request, session
from quiz.quiz_files.quiz_app_utils import QuizDatabaseConnectionHandler
from quiz.quiz_files.quiz_module import QuizModule


# class encapsulates quiz routes in the application, including interaction with the front-end and quiz requests
class QuizAPI:
    def __init__(self):
        self.db = None
        self.jokes = itertools.cycle([
            'Why did the tomato turn red? Because it saw the salad dressing!',
            'Why don’t eggs tell jokes? Because they might crack up!',
            'What’s a chef’s favorite martial art? Chop suey!',
            'What do you call cheese that isn\'t yours? Nacho cheese!',
            'Why did the student eat his homework? Because the teacher said it was a piece of cake!',
        ])

    # this method sets up a db connection before handling any http requests
    def before_request(self):
        self.db = QuizDatabaseConnectionHandler.get_db()

    # this method is called from main.py and uses the Flask 'before_request' decorator to register
    # the before_request method ensures the db connection is set up ahead of each http request
    def init_app(self, app):
        app.before_request(self.before_request)

        # routes for quiz are defined within the init_app method, once defined, they are registered to the
        # Flask app instance(passed as the 'app' argument) by main.py
        @app.route('/quiz', methods=['GET'])
        def start_quiz():
            return render_template('quiz.html')

        @app.route('/quiz/get_question/<int:question_id>', methods=['GET'])
        def get_question(question_id):
            question = self.db.get_question(question_id)

            # check a question is returned from the db
            if question is None:
                return jsonify({'error': f'Question not found in the db with id {question_id}'}), 404

            return jsonify({'question': question})

        @app.route('/quiz/get_question_answers/<int:question_id>', methods=['GET'])
        def get_question_answers(question_id):
            question_answers = self.db.get_question_answers(question_id)

            # check question answer choices are returned from the db
            if question_answers is None:
                return jsonify({'error': f'Question answers not found in the db with id {question_id}'}), 404

            return jsonify({'question_answers': question_answers})

        @app.route('/quiz/next_question', methods=['POST'])
        def next_question():
            # end of quiz
            if len(session['list_of_asked_questions_by_id']) == 5:
                # get next joke using the itertools 'cycle'
                joke = next(self.jokes)
                return render_template('quiz_finish.html',
                                       user_score=session['user_score'],
                                       joke=joke)
            # continue quiz
            else:
                # update session variables with next question
                session['question_id'] = QuizModule.get_question_id()
                question_row_from_db = self.db.get_question(session['question_id'])
                question = question_row_from_db[0][1]
                correct_answer_id = question_row_from_db[0][2]
                session['correct_answer_id'] = correct_answer_id
                question_answers_from_db = self.db.get_question_answers(session['question_id'])
                answer1 = question_answers_from_db[0][0]
                answer2 = question_answers_from_db[1][0]
                answer3 = question_answers_from_db[2][0]
                answer4 = question_answers_from_db[3][0]

                # update template with next question information.
                return render_template('quiz.html',
                                       question=question,
                                       session_quiz_number=len(session['list_of_asked_questions_by_id']),
                                       correct_answer_id=session['correct_answer_id'],
                                       user_score=session['user_score'],
                                       answer1=answer1,
                                       answer2=answer2,
                                       answer3=answer3,
                                       answer4=answer4
                                       )

        @app.route('/quiz/get_answers', methods=['GET'])
        def get_answers():
            answers = self.db.get_answers()
            return jsonify({'answers': answers})

        @app.route('/quiz/check_answer', methods=['POST'])
        def check_answer():
            # get user answer from the HTML form action
            submitted_answer = request.form['answer']
            # get correct_answer from the db
            raw_correct_answer = self.db.fetch_correct_answer(session['correct_answer_id'])
            if raw_correct_answer and raw_correct_answer[0]:
                correct_answer = raw_correct_answer[0][0]
            else:
                correct_answer = None
            # compare user's answer with correct_answer from the db and render template accordingly.
            if submitted_answer == correct_answer:
                session['user_score'] += 1
                question_feedback = 'Correct!'

            else:
                question_feedback = 'Incorrect!'

            return render_template('quiz_response.html',
                                   user_score=session['user_score'],
                                   submitted_answer=submitted_answer,
                                   question_feedback=question_feedback,
                                   correct_answer=correct_answer)

        @app.route('/quiz/new_quiz', methods=['POST'])
        def new_quiz():
            # create new instance of QuizModule
            return QuizModule.start()

import pytest
from flask import jsonify, session
import unittest.mock as mock
from quiz.quiz_files.quiz_module import QuizModule
from main import CookingApp


# Initialises 'CookingApp' instance and returns the Flask app for testing
@pytest.fixture
def app():
    cooking_app = CookingApp()
    cooking_app.app.config['SECRET_KEY'] = ''  # enter secret key here
    return cooking_app.app


# Creates a test client to simulate HTTP requests to the Flask application.
@pytest.fixture
def client(app):
    return app.test_client()


# This fixture sets up specific test routes for testing within the Flask app instance 'app'.
@pytest.fixture(autouse=True)
def add_test_routes(app):

    # Test route for 'initialise_session_for_quiz' method in QuizModule.
    @app.route('/test_initialise_session_for_quiz')
    def test_initialise_session_for_quiz():
        QuizModule.initialise_session_for_quiz()
        return 'Session initialised', 200

    # Test route for 'get_question_id' method in QuizModule.
    @app.route('/test_get_question_id')
    def test_get_question_id():
        question_id = QuizModule.get_question_id()
        # Ensure the changes in session, ie a new question_id, are recognised and persist in Flask.
        session.modified = True
        return jsonify({'question_id': question_id}), 200

    # Test route for 'generate_quiz' method in QuizModule.
    @app.route('/test_generate_quiz')
    def test_generate_quiz():
        quiz = QuizModule()
        quiz.generate_quiz()
        return jsonify({'session_quiz_number': len(session['list_of_asked_questions_by_id']),
                        'correct_answer_id': session['correct_answer_id'],
                        'user_score': session['user_score'],
                        'question': quiz.question,
                        'answer1': quiz.answer1,
                        'answer2': quiz.answer2,
                        'answer3': quiz.answer3,
                        'answer4': quiz.answer4
                        })


# Class to test the initialisation of QuizModule.
class TestQuizModuleInitialisation:

    # Test to see if all properties of a QuizModule instance are 'None' when initialised
    def test_initialisation(self):
        quiz_module = QuizModule()
        assert quiz_module.question is None, 'question should be None on initialisation'
        assert quiz_module.answer1 is None, 'answer1 should be None on initialisation'
        assert quiz_module.answer2 is None, 'answer2 should be None on initialisation'
        assert quiz_module.answer3 is None, 'answer3 should be None on initialisation'
        assert quiz_module.answer4 is None, 'answer4 should be None on initialisation'

    # Test to check initialisation of the session for the quiz.
    # Checks HTTP response status codes and that session variables are correctly set.
    def test_initialise_session_for_quiz(self, client):
        response = client.get('/test_initialise_session_for_quiz')
        assert response.status_code == 200
        # Check session variables on initialisation
        with client.session_transaction() as sess:
            assert sess['user_score'] == 0
            assert sess['list_of_asked_questions_by_id'] == []
            assert sess['question_id'] is None
            assert sess['correct_answer_id'] is None

    # Test to check start_quiz method calls the 'initialise_session_for_quiz' and 'generate_quiz' methods in QuizModule.
    @mock.patch.object(QuizModule, 'initialise_session_for_quiz')
    @mock.patch.object(QuizModule, 'generate_quiz')
    def test_start_quiz(self, mock_generate_quiz, mock_initialise_session_for_quiz):
        quiz = QuizModule()
        quiz.start_quiz()
        mock_initialise_session_for_quiz.assert_called_once()
        mock_generate_quiz.assert_called_once()


# Class contains unit tests for QuizModule class and its methods
class TestQuizModule:

    # Test for a redirect to login on /quiz route if user isn't logged in.
    def test_start_quiz(self, client):
        response = client.get('/quiz')
        assert response.status_code == 302
        assert b'/login' in response.data

    # Test functionality of the get_question_id method.
    def test_get_question_id(self, client):
        # Call the route to initialise the session
        response = client.get('/test_initialise_session_for_quiz')
        assert response.status_code == 200

        # Check the session state after initialisation
        with client.session_transaction() as sess:
            assert sess['list_of_asked_questions_by_id'] == []

        # First call to get_question_id
        response = client.get('/test_get_question_id')
        assert response.status_code == 200

        # Check question_id generated in range(1, 31)
        data = response.get_json()
        question_id = data['question_id']
        assert question_id in range(1, 31)

        # Check the session state after route for get_question_id called
        with client.session_transaction() as sess:
            list_of_asked_questions_by_id = sess['list_of_asked_questions_by_id']
            assert question_id in list_of_asked_questions_by_id
            assert len(list_of_asked_questions_by_id) == 1

    # Test to ensure the generate_quiz method makes expected function calls.
    # Uses mocking to test the internal function calls inside the generate_quiz method.
    def test_generate_quiz_call(self, app):
        # Ensure active request context() when accessing the session
        with app.test_request_context():
            # Mock internal function calls
            with (mock.patch.object(QuizModule, 'get_question_id') as mock_get_question_id,
                  mock.patch.object(QuizModule, 'get_question') as mock_get_question,
                  mock.patch.object(QuizModule, 'get_question_answers') as mock_get_question_answers):
                mock_get_question_id.return_value = 12
                quiz = QuizModule()
                quiz.generate_quiz()
                mock_get_question_id.assert_called_once()
                mock_get_question.assert_called_once()
                mock_get_question_answers.assert_called_once()

    # Test changes to session and QuizModule instance attributes from 'generate_quiz' method.
    # Uses mocking to simulate HTTP requests and responses.
    @mock.patch('requests.get')
    def test_generate_quiz(self, mock_get, client, app):
        # Mock HTTP request for get_question and get_question_answers
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {'question': [
                [12, 'Test question', 47, 1]
            ]},
            {'question_answers': [
                ['Test answer1'],
                ['Test answer2'],
                ['Test answer3'],
                ['Test answer4']
            ]}]

        # Check route exists and returns expected JSON structure
        with app.test_request_context():
            with (mock.patch.object(QuizModule, 'get_question_id', return_value=12),
                  mock.patch.object(QuizModule, 'get_question', return_value={'question': [12, 'Test question', 47, 1]}),
                  mock.patch.object(QuizModule, 'get_question_answers', return_value={
                      'question_answers': [
                          ['Test answer1'],
                          ['Test answer2'],
                          ['Test answer3'],
                          ['Test answer4']
                      ]
                  }) as mock_get_question_answers
                  ):

                # Instantiate QuizModule()
                quiz = QuizModule()
                # Generate quiz with mock values
                quiz.generate_quiz()

                with client.session_transaction() as sess:
                    sess['list_of_asked_questions_by_id'] = [12]
                    sess['correct_answer_id'] = 47
                    sess['user_score'] = 0

                # Call route for test_generate_quiz
                response = client.get('/test_generate_quiz')
                assert response.status_code == 200

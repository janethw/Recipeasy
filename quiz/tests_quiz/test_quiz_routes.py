import pytest
from bs4 import BeautifulSoup
from main import CookingApp


# Class to tests the routes relating to the quiz functionality within the Flask app
class TestQuizRoute:

    # Fixture set up a test client for the Flask app.
    @pytest.fixture
    def client(self):
        cooking_app = CookingApp()
        cooking_app.app.config.update({
            'TESTING': True,
            'SECRET_KEY': '',  # add secret key
            'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
        })
        # Use the client to provide app context and client for tests
        with cooking_app.app.test_client() as client:
            with cooking_app.app.app_context():
                pass
            yield client

    # Fixture simulates a user with a valid session, called 'test_user'
    @pytest.fixture
    def logged_in_client(self, client):
        with client.session_transaction() as sess:
            # Mock the session as if the user is logged in
            sess['username'] = 'test_user'
        return client

    # Test to confirm response status is 200 once a user is logged in.
    # Verify an HTML element is as expected.
    def test_quiz_route_response_status(self, logged_in_client):
        response = logged_in_client.get('/quiz')
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')
        assert soup.find('div', {'class': 'quizGridContainer'}) is not None

    # Test to confirm session cookies are set correctly once logged in.
    # Verifies an HTML element is as expected.
    def test_quiz_route_session_cookie(self, logged_in_client):
        question_id = 1
        response = logged_in_client.get(f'/quiz/get_question_answers/{question_id}')
        assert response.status_code == 200

        with logged_in_client.session_transaction() as session:

            # set session data
            session['answer1'] = 'test_answer1'
            session['answer2'] = 'test_answer2'
            session['answer3'] = 'test_answer3'
            session['answer4'] = 'test_answer4'
            session['correct_answer_id'] = 'test_correct_answer_id'
            session['user_score'] = 0
            session['list_of_questions_asked_by_id'] = [6, 7]
            session['question_id'] = 3
            session.modified = True

        response = logged_in_client.get('/quiz')
        assert response.status_code == 200
        # Check an HTML element
        soup = BeautifulSoup(response.data, 'html.parser')
        assert soup.find('div', {'class': 'quizGridContainer'}) is not None

    # Test checks the get_question_answers route.
    # Tests a valid scenario where question_id is 1 and an invalid scenario where question_id is 7777
    def test_get_question_answers_route(self, logged_in_client):
        # Test fetching valid question answers
        response = logged_in_client.get('/quiz/get_question_answers/1')
        assert response.status_code == 200
        assert response.json['question_answers'] == [['France'], ['Spain'], ['USA'], ['Japan']]

        response = logged_in_client.get('/quiz/get_question_answers/12')
        assert response.status_code == 200
        assert response.json['question_answers'] == [['Rice'], ['Apples'], ['Cheese'], ['Crisps']]

        response = logged_in_client.get('/quiz/get_question_answers/29')
        assert response.status_code == 200
        assert response.json['question_answers'] == [['Prunes'], ['Dates'], ['Raisins'], ['Apricots']]

        response = logged_in_client.get('/quiz/get_question_answers')
        assert response.status_code == 500
        assert not response.json

        # Test fetching invalid question answers
        response = logged_in_client.get('/quiz/get_question_answers/7777')
        assert response.status_code == 404

    def test_get_answers_route(self, logged_in_client):
        # Test fetching all answers
        response = logged_in_client.get('/quiz/get_answers')
        assert response.status_code == 200
        assert response.json['answers'] == [['France'], ['Spain'], ['USA'], ['Japan'], ['Apple'], ['Orange'], ['Banana'], ['Grape'], ['Water'], ['Milk'], ['Orange Juice'], ['Squash'], ['Honey'], ['Chocolate'], ['Jelly'], ['Peanut Butter'], ['Cake'], ['Carrot'], ['Pasta'], ['Cheese'], ['Apple Juice'], ['Squash'], ['Lemonade'], ['Milk'], ['Potatoes'], ['Rice'], ['Corn'], ['Wheat'], ['Spoon'], ['Knife'], ['Plate'], ['Fork'], ['Flour'], ['Butter'], ['Sugar'], ['Salt'], ['Boiling'], ['Frying'], ['Grilling'], ['Steaming'], ['Gravy'], ['Sauce'], ['Dough'], ['Batter'], ['Rice'], ['Apples'], ['Cheese'], ['Crisps'], ['Chips'], ['Donuts'], ['Chicken'], ['Oranges'], ['Grapes'], ['Cookies'], ['Pizza'], ['Oranges'], ['Sweets'], ['Fruits'], ['Vegetables'], ['Nuts'], ['India'], ['Argentina'], ['Nigeria'], ['Germany'], ['Pizza'], ['Sushi'], ['Tacos'], ['Cottage Pie'], ['Croissant'], ['Scone'], ['Baguette'], ['Pretzel'], ['Carbohydrates'], ['Cereal'], ['Carrots'], ['Couscous'], ['Broccoli'], ['Pasta'], ['Marshmallows'], ['Chocolate'], ['Batter'], ['Sauce'], ['Gravy'], ['Icing'], ['Chocolate'], ['Crisps'], ['Rice'], ['Noodles'], ['Pizza'], ['Spaghetti'], ['Lasagne'], ['Enchiladas'], ['Avocado'], ['Chickpeas'], ['Onion'], ['Potato'], ['South Africa'], ['Mexico'], ['Russia'], ['Germany'], ['Vegan'], ['Carnivore'], ['Vegetarian'], ['Pescatarian'], ['Vitamin A'], ['Vitamin B'], ['Vitamin C'], ['Vitamin D'], ['Carbohydrates'], ['Protein'], ['Dairy'], ['Fruits & Vegetables'], ['Prunes'], ['Dates'], ['Raisins'], ['Apricots'], ['Dairy'], ['Vegetables'], ['Protein'], ['Carbohydrates']]

    def test_check_answers_route(self, logged_in_client):

        # Checking incorrect answer
        with logged_in_client.session_transaction() as session:
            session['correct_answer_id'] = 2
            session['user_score'] = 88
            session.modified = True

        payload = {'answer': 'France'}
        response = logged_in_client.post('/quiz/check_answer', data=payload)
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')
        answer_feedback = soup.find('h2', {'id': 'answer_feedback'}).get_text()
        assert 'France' in answer_feedback and 'incorrect' in answer_feedback

        # Checking score has not increased
        with logged_in_client.session_transaction() as session:
            assert session['user_score'] == 88

        # Checking correct answer
        with logged_in_client.session_transaction() as session:
            session['correct_answer_id'] = 18
            session['user_score'] = 39
            session.modified = True

        payload = {'answer': 'Carrot'}
        response = logged_in_client.post('/quiz/check_answer', data=payload)
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')
        answer_feedback = soup.find('h2', {'id': 'answer_feedback'}).get_text()
        assert 'Carrot' in answer_feedback and 'incorrect' not in answer_feedback

        # Checking score has increased by one
        with logged_in_client.session_transaction() as session:
            assert session['user_score'] == 40

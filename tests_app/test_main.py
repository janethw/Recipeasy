import pytest
from main import CookingApp


# class to test routes in CookingApp for successful response, redirection and getting specific content
class TestCookingAppRoutes:
    # this fixture creates a Flask instance to represent the web app to allow its endpoints to be tested
    @pytest.fixture
    def client(self):
        cooking_app = CookingApp()
        cooking_app.app.config.update({
            'TESTING': True,
        })
        with cooking_app.app.test_client() as client:
            yield client

    def test_index_route(self, client):
        response = client.get('/')
        # expect a redirect ie a status of 302 for index route to go to login page
        assert response.status_code == 302

    def test_quiz_route(self, client):
        response = client.get('/quiz')
        # expect redirect to login page
        assert response.status_code == 302

    def test_recipe_route(self, client):
        response = client.get('/recipe')
        # expect redirect to login page
        assert response.status_code == 302

    def test_get_recipe_route(self, client):
        response = client.get('/get_recipe')
        # expect redirect to login page
        assert response.status_code == 302

    def test_get_recipe_route_with_recipe_id(self, client):
        response = client.get('/get_recipe?ingredient1=chicken')
        assert response.status_code == 302

import pytest
from main import CookingApp


class TestLoginRoute:

    @pytest.fixture
    def client(self):
        cooking_app = CookingApp()
        cooking_app.app.config.update({
            'TESTING': True,
            'SECRET_KEY': 'test_secret_key',
            'WTF_CSRF_ENABLED': False  # disable CSRF for testing
        })
        with cooking_app.app.test_client() as client:
            with cooking_app.app.app_context():
                pass
            yield client

    @pytest.fixture
    def logged_in_client(self, client):
        with client.session_transaction() as sess:
            # mock the session as if the user is logged in
            sess['username'] = 'test_user'
            sess['email'] = 'tester@testing.com'
        return client

    # testing no homepage access if not logged in
    def test_homepage_route_redirect(self, client):
        response = client.get('/homepage')
        assert response.status_code == 302
        assert response.headers['Location'] == '/login'

    # testing homepage access if logged in
    def test_homepage_route_success(self, logged_in_client):
        response = logged_in_client.get('/homepage')
        assert response.status_code == 200

    # testing no profile access if not logged in
    def test_profile_route_redirect(self, client):
        response = client.get('/profile')
        assert response.status_code == 302
        assert response.headers['Location'] == '/login'

    # testing profile access if logged in
    def test_profile_route_success(self, logged_in_client):
        response = logged_in_client.get('/profile')
        assert response.status_code == 200

    # testing login route incorrect password
    def test_login_route_fail(self, client):

        with client.session_transaction() as session:
            session['username'] = 'elle'
            session['email'] = 'elle@test.org'
            session.modified = True

        payload = {'username': 'elle', 'password': 'elle2', 'email': 'elle@test.org'}
        response = client.post('/login', data=payload)
        assert response.status_code == 200
        assert 'Username or Password Incorrect' in response.text

    # testing login route correct password
    def test_login_route_success(self, client):

        with client.session_transaction() as session:
            session['username'] = 'elle'
            session['email'] = 'elle@test.org'
            session.modified = True

        payload = {'username': 'elle', 'password': 'elle', 'email': 'elle@test.org'}
        response = client.post('/login', data=payload, follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == '/homepage'

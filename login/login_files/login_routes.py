from flask import request, render_template, session, redirect, url_for
from app_utils import login_required
from login.login_files.login_app_utils import LoginDatabaseConnectionHandler
from login.login_files.login_module import User


class UserAPI:
    def __init__(self):
        self.db = None

    # ensure there is a db connection before a request is made
    def before_request(self):
        self.db = LoginDatabaseConnectionHandler.get_db()

    # this method is called in main.py as part of the db configuration
    # it uses Flask's before_request method to ensure that the class
    # before_request(self) method is called ahead of each http request
    def init_app(self, app):
        app.before_request(self.before_request)

        @app.route('/homepage')
        @login_required
        def homepage():
            return render_template('homepage.html')

        @app.get('/profile')
        @login_required
        def profile():
            username = session['username']
            email = session['email']
            return render_template('profile.html', username=username, email=email)

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            error = None
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                # hash of password from user login form
                hashed_password = User.hash_pw(password)
                # hashed_password = generate_password_hash(password)
                db_result = self.db.get(username)
                if db_result is not None:
                    db_stored_hash = db_result[0]
                    email = db_result[1]
                    if db_stored_hash and db_stored_hash == hashed_password:
                        # add username to session dictionary
                        session['username'] = username
                        session['email'] = email
                        return redirect(url_for('homepage'))
                    else:
                        error = 'Username or Password Incorrect'
                else:
                    error = 'Username or Password Incorrect'
            return render_template('login.html', error=error)

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            error = None
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                # hash the user's input password to store in the db
                hashed_password = User.hash_pw(password)
                # attempt to register new user
                try:
                    self.db.register(username, email, hashed_password)
                    # add username to session dictionary
                    session['username'] = username
                    session['email'] = email
                    return redirect(url_for('homepage'))
                except ValueError as e:
                    if str(e) == 'Username Taken':
                        error = 'Username already taken. Please try again.'
                    else:
                        error = 'An unexpected error occurred. Please try again.'
                    return render_template('register.html', error=error)
            return render_template('register.html', error=error)

        @app.route('/logout')
        @login_required
        def logout():
            session.pop('user', None)
            session.clear()
            return render_template('logout.html')

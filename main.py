from flask import Flask, url_for, request, redirect, render_template
from game.game_files.game_module import GameModule
from recipe_builder.recipe_builder_files.recipe_module import RecipeModule
from quiz.quiz_files.quiz_module import QuizModule
from quiz.quiz_files.quiz_routes import QuizAPI
from login.login_files.login_routes import UserAPI
from logging_utils import init_logger, logger_message
from app_utils import DatabaseConnectionHandler
from db_utils import ExceptionDatabaseConnectionFailed
from config import FLASK_APP_SECRET_KEY

# initialises logger
_logger = init_logger()


# class representing core application object
class CookingApp:
    def __init__(self):
        # create the Flask app instance and initialise core application services
        self.app = Flask(__name__)

        # log start of Flask application
        _logger.info(
            logger_message.format(module_name=__name__, function_name='__init__', message='Starting Flask application'))
        self.app.secret_key = FLASK_APP_SECRET_KEY
        self.configure_routes()
        self.configure_database()

    def configure_routes(self):
        # configures routes for the Flask application and sets up route-view function pairs and error handling

        _logger.info(logger_message.format(module_name=__name__, function_name='configure_routes', message='Configuring routes'))

        # error handler for database connection
        @self.app.errorhandler(ExceptionDatabaseConnectionFailed)
        def handle_database_error(error):
            return render_template('error_page.html', error_message=f'Failed to connect to database: {error}'), 500

        # general error handling
        @self.app.errorhandler(Exception)
        def unhandled_error(error):
            return render_template('error_page.html', error_message=f'An unexpected error has occurred: {error}'), 500

        # configures URLs and their view functions
        @self.app.route('/')
        def index():
            return redirect(url_for('login'))

        @self.app.route('/quiz')
        def quiz():
            return QuizModule.start()

        @self.app.route('/recipe')
        def recipe():
            return RecipeModule.start()

        @self.app.route('/get_recipe')
        def get_recipe():
            return RecipeModule.get_recipe(request.args)

        @self.app.route('/recipe_details/recipe_id:<recipe_id>')
        def recipe_details(recipe_id):
            return RecipeModule.get_recipe_details(recipe_id)

        @self.app.route('/game')
        def game():
            return GameModule.start()

    def configure_database(self):
        # create and configure APIs
        quiz_api = QuizAPI()
        quiz_api.init_app(self.app)
        user_api = UserAPI()
        user_api.init_app(self.app)

        # close database connection after request
        @self.app.teardown_appcontext
        def close_db_connection(_exception):
            DatabaseConnectionHandler.close_db()

    def run(self, debug=False):
        # runs app on local development server
        self.app.run(debug=True)


if __name__ == '__main__':
    CookingApp().run(debug=True)

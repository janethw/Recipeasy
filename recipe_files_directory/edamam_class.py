import requests
from recipe_files_directory.api_config import API_ID, API_KEY
from recipe_files_directory.recipe_class import Recipe
from logging_utils import init_logger, logger_message

_logger = init_logger()  # fetching logger


class ExceptionMissingAPIIDKey(Exception):
    pass


class ExceptionAPIInvalid(Exception):
    pass


class ExceptionNoIngredients(Exception):
    pass


class EdamamRecipes:

    def __init__(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='__init__', message='entry'))
        self.recipe_list = []
        self.search_parameters = None
        self.ingredient_list = []
        self._api_id = API_ID
        self._api_key = API_KEY
        self._data = None
        self._next_results_href = None

        if self._api_key is None or self._api_id is None or self._api_key == '' or self._api_id == '':
            _logger.critical(logger_message.format(module_name=__name__, function_name='__init__',
                                                   message='Missing API ID or API key'))
            raise ExceptionMissingAPIIDKey('Missing API ID or API key')

    # processing edamam recipe object and storing it in the database
    @staticmethod
    def process_edamam_recipe_data(recipe_json):
        _logger.debug(
            logger_message.format(module_name=__name__, function_name='process_edamam_recipe_data', message='entry'))
        edamam_uri = recipe_json['uri']
        edamam_url = recipe_json['url']
        edamam_image = recipe_json['image']
        edamam_yield = recipe_json['yield']
        edamam_title = recipe_json['label']
        recipe = Recipe(edamam_uri, edamam_url, edamam_image, edamam_yield, edamam_title)

        _logger.debug(logger_message.format(module_name=__name__, function_name='process_edamam_recipe_data',
                                            message='Recipe class created, adding ingredients'))

        for ingredient in recipe_json['ingredients']:
            recipe.add_ingredient(ingredient['food'], ingredient['foodCategory'], ingredient['quantity'],
                                  ingredient['measure'])

        _logger.debug(logger_message.format(module_name=__name__, function_name='process_edamam_recipe_data',
                                            message='Ingredients added to recipe, storing in database'))

        try:
            recipe.store_recipe_in_database()
        except Exception as e:
            _logger.error(logger_message.format(module_name=__name__, function_name='process_edamam_recipe_data',
                                                message=f'Failed to store recipe in the database: {e}'))

        return recipe

    # processing the edamam response, loops through the recipes in the response and adds them to a list
    def _process_edamam_data(self):
        _logger.debug(
            logger_message.format(module_name=__name__, function_name='_process_edamam_data', message='entry'))

        for recipe in self._data['hits']:
            self.recipe_list.append(self.process_edamam_recipe_data(recipe['recipe']))

        # for future proofing, fetching the url to the additional results
        if '_links' in self._data:
            if 'next' in self._data['_links']:
                _logger.debug(logger_message.format(module_name=__name__, function_name='_process_edamam_data',
                                                    message='setting next page url'))
                self._next_results_href = self._data['_links']['next']['href']
            else:
                self._next_results_href = None
        else:
            self._next_results_href = None

    def set_ingredients(self, ingredient_list):
        self.ingredient_list = ingredient_list

    def get_ingredient_list_string(self):
        return ','.join(self.ingredient_list)

    # calls edamam api with the set ingredients then processes the response
    def recipe_search(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='recipe', message='entry'))

        if len(self.ingredient_list) == 0:
            _logger.error(logger_message.format(module_name=__name__, function_name='recipe_search',
                                                message='No ingredients passed to function'))
            raise ExceptionNoIngredients('No ingredients set')

        result = requests.get(
            'https://api.edamam.com/search?q={ingredients}&app_id={app_id}&app_key={app_key}'
            .format(ingredients=self.get_ingredient_list_string(), app_id=self._api_id, app_key=self._api_key)
        )

        if result.status_code != 200:
            self._data = None
            _logger.error(logger_message.format(module_name=__name__, function_name='recipe_search',
                                                message=f'API call returned {result.status_code} status code for URL{'https://api.edamam.com/search?q={ingredients}&app_id={app_id}&app_key={app_key}'
                                                .format(ingredients=self.get_ingredient_list_string(), app_id='API_ID', app_key='API_KEY')}'))
            raise ExceptionAPIInvalid('API returned an invalid status code')

        self._data = result.json()
        self._process_edamam_data()
        self._data = None

    # returns a list of recipe data of the edamam recipes in a format that can be easily used in the html table
    def output_tabular_data(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='output_tabular_data', message='entry'))
        return [recipe.output_tabular_data() for recipe in self.recipe_list]

    # class method to return an instance of the edamam class by passing in the ingredient list
    @classmethod
    def edamam_ingredient_search(cls, ingredient_list):
        _logger.info(
            logger_message.format(module_name=__name__, function_name='edamam_ingredient_search', message='entry'))
        edamam_recipes = cls()
        edamam_recipes.set_ingredients(ingredient_list)
        try:
            edamam_recipes.recipe_search()
        except ExceptionNoIngredients as e:
            raise e
        except ExceptionAPIInvalid as e:
            raise e
        except ExceptionMissingAPIIDKey as e:
            raise e
        return edamam_recipes

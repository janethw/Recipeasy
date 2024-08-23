from recipe_builder.recipe_db_utils import RecipeSQLDatabase, DataNotFound
from logging_utils import init_logger, logger_message
from recipe_scrapers import scrape_me, scraper_exists_for

_logger = init_logger()


class Recipe:
    def __init__(self, edamam_uri, edamam_url, edamam_image, edamam_yield, edamam_title, recipe_id=None):
        _logger.debug(logger_message.format(module_name=__name__, function_name='__init__', message='entry'))
        self._edamam_uri = edamam_uri
        self._edamam_url = edamam_url
        self._edamam_image = edamam_image
        self._edamam_yield = edamam_yield
        self._edamam_title = edamam_title
        self._recipe_id = recipe_id
        self._ingredients = {}
        self._instructions = []
        self._db_connection = None

    # adding the ingredients to the class dictionary variable
    def add_ingredient(self, ingredient_name, ingredient_category, quantity, measure, ingredient_id=None):
        self._ingredients[ingredient_name] = {'category': ingredient_category,
                                              'quantity': quantity,
                                              'measure': measure if measure != '<unit>' else '',
                                              'ingredient_id': ingredient_id}

    # stores the recipe in the database and fetches the ids of the inserted data in one transaction to avoid the
    # recipe existing without its ingredients
    def store_recipe_in_database(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='store_recipe_in_database',
                                            message=f'entry, storing recipe {self._edamam_title}'))
        db_connection = RecipeSQLDatabase()
        try:
            self._recipe_id = db_connection.recipe_details(self._edamam_uri,
                                                           self._edamam_url,
                                                           self._edamam_image,
                                                           self._edamam_yield,
                                                           self._edamam_title)

            for ingredient in self._ingredients:
                _logger.debug(logger_message.format(module_name=__name__, function_name='store_recipe_in_database',
                                                    message=f'storing ingredient {ingredient}'))
                self._ingredients[ingredient]['ingredient_id'] = db_connection.ingredient_data(ingredient,
                                                                                               self._ingredients
                                                                                               [ingredient]['category'])
                db_connection.recipe_ingredients(self._recipe_id,
                                                 self._ingredients[ingredient]['ingredient_id'],
                                                 self._ingredients[ingredient]['quantity'],
                                                 self._ingredients[ingredient]['measure'])
            db_connection.commit()
            _logger.debug(logger_message.format(module_name=__name__, function_name='store_recipe_in_database',
                                                message='recipe in database and committed'))
        except Exception as e:
            _logger.error(logger_message.format(module_name=__name__, function_name='store_recipe_in_database',
                                                message=f'Error storing recipe, message {e}'))
            raise e
        finally:
            db_connection.close()

    # outputs the data for the html in an appropriate format
    def output_tabular_data(self):
        _logger.debug(logger_message.format(module_name=__name__, function_name='output_tabular_data', message='entry'))
        return {'recipe_id': self._recipe_id, 'url': self._edamam_url, 'image_url': self._edamam_image,
                'title': self._edamam_title}

    # uses the recipe_scraper library to fetch the instructions from the external recipe url
    def scrape_instructions(self):
        # call the scraper and set a parameter in the class with the list of instructions
        # check if there is a scraper which exists for the URL first
        if scraper_exists_for(self._edamam_url):
            scraped_recipe = scrape_me(self._edamam_url)
            self._instructions = scraped_recipe.instructions_list()

    # returns the instructions to whatever has called this function
    def get_instructions(self):
        if self._instructions is None or len(self._instructions) == 0:
            self.scrape_instructions()

        return self._instructions

    # gets all the data for a recipe from the database and returns a Recipe class object
    @classmethod
    def get_recipe_from_id(cls, recipe_id):
        _logger.info(logger_message.format(module_name=__name__, function_name='get_recipe_from_id', message='entry'))
        db_connection = RecipeSQLDatabase()
        try:
            recipe_dict = db_connection.get_recipe_details(recipe_id)

            recipe = cls(recipe_dict['uri'], recipe_dict['url'], recipe_dict['image'], recipe_dict['yield'],
                         recipe_dict['title'], recipe_id)

            ingredients = db_connection.get_recipe_ingredients(recipe_id)

            for ingredient in ingredients:
                recipe.add_ingredient(ingredient['ingredient'], ingredient['category'], ingredient['quantity'],
                                      ingredient['measure'], ingredient['ingredient_id'])

            return recipe
        except DataNotFound as e:
            _logger.error(logger_message.format(module_name=__name__, function_name='get_recipe_from_id',
                                                message=f'recipe_id {recipe_id} not found in the database'))
            raise e
        except Exception as e:
            _logger.error(logger_message.format(module_name=__name__, function_name='get_recipe_from_id',
                                                message=f'Unexpected error occurred: {e}'))
            raise e
        finally:
            db_connection.close()

    def get_ingredients(self):
        return self._ingredients

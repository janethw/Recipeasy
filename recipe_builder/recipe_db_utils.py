from db_utils import SQLDatabase, DataNotFound
from logging_utils import init_logger, logger_message

_logger = init_logger()  # fetching logger


class RecipeSQLDatabase(SQLDatabase):

    # inserting the recipe details into the SQL database, and returning the recipe ID
    def recipe_details(self, edamam_uri, edamam_url, edamam_image, edamam_yield, edamam_title, commit=False):
        _logger.debug(logger_message.format(module_name=__name__, function_name='recipe_details', message='entry'))
        insert_str = '''INSERT INTO recipe_details (uri, url, image, yield, title)
                VALUES (%(edamam_uri)s, %(edamam_url)s, %(edamam_image)s, %(edamam_yield)s, %(edamam_title)s) 
                on duplicate key update url=%(edamam_url)s, image=%(edamam_image)s, yield=%(edamam_yield)s, title=%(edamam_title)s'''

        insert_values = {'edamam_uri': edamam_uri, 'edamam_url': edamam_url, 'edamam_image': edamam_image,
                         'edamam_yield': edamam_yield,
                         'edamam_title': edamam_title}

        self.insert_update_data(insert_str, insert_values, commit=commit)

        # values inserted now fetching id
        query_results = self.query_data('select recipe_id from recipe_details where uri = %s',
                                        (edamam_uri,))  # ',' needed otherwise it thinks it's a string and throws error
        # checking actually returned something
        if len(query_results) >= 1:
            recipe_idx = query_results[0][0]
        else:
            raise DataNotFound('No data returned')

        return recipe_idx

    # inserting the ingredient data into the SQL database and returning the ingredient ID
    def ingredient_data(self, edamam_ingredient, edamam_category, commit=False):
        _logger.debug(logger_message.format(module_name=__name__, function_name='ingredient_data', message='entry'))
        insert_str = '''INSERT INTO ingredients (ingredient, category)
                VALUES (%(edamam_ingredient)s, %(edamam_category)s)
                on duplicate key update category = %(edamam_category)s'''

        insert_values = {'edamam_ingredient': edamam_ingredient, 'edamam_category': edamam_category}

        self.insert_update_data(insert_str, insert_values, commit=commit)

        # values inserted now fetching id using uri
        query_results = self.query_data('select ingredient_id from ingredients where ingredient = %s',
                                        (
                                            edamam_ingredient,))  # ',' needed otherwise it thinks it's a string and throws error
        # checking actually returned something
        if len(query_results) >= 1:
            ingredient_id = query_results[0][0]
        else:
            raise DataNotFound('No data returned')

        return ingredient_id

    # inserting the ingredient data associated with the recipe into the SQL database
    def recipe_ingredients(self, recipe_id, ingredient_id, edamam_quantity, edamam_measure, commit=False):
        _logger.debug(logger_message.format(module_name=__name__, function_name='recipe_ingredients', message='entry'))
        insert_str = '''INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, measure)
                VALUES (%(recipe_id)s, %(ingredient_id)s, %(edamam_quantity)s, %(edamam_measure)s)
                on duplicate key update quantity = %(edamam_quantity)s, measure = %(edamam_measure)s'''

        insert_values = {'recipe_id': recipe_id, 'ingredient_id': ingredient_id, 'edamam_quantity': edamam_quantity,
                         'edamam_measure': edamam_measure}

        self.insert_update_data(insert_str, insert_values, commit=commit)

    # fetching details of the recipe from the database using the recipe ID
    def get_recipe_details(self, recipe_id):
        # returns a dictionary of the recipe_details row
        recipe_detail_query = '''SELECT r.uri, r.url, r.image, r.yield, r.title FROM recipe_details AS r 
            WHERE r.recipe_id = %(recipe_id)s'''

        query_values = {'recipe_id': recipe_id}

        rows = self.query_data(recipe_detail_query, query_values)

        if rows is None or len(rows) == 0:
            raise DataNotFound('No rows returned')

        recipe_details_dict = {'uri': rows[0][0],
                               'url': rows[0][1],
                               'image': rows[0][2],
                               'yield': rows[0][3],
                               'title': rows[0][4]}

        return recipe_details_dict

    # fetching the ingredients of a recipe from the database using the recipe ID
    def get_recipe_ingredients(self, recipe_id):

        ingredient_detail_query = '''SELECT ri.quantity, ri.measure, i.ingredient, i.ingredient_id, i.category 
        FROM recipe_details AS r INNER JOIN recipe_ingredients AS ri ON ri.recipe_id=r.recipe_id 
        INNER JOIN ingredients AS i ON i.ingredient_id=ri.ingredient_id WHERE ri.recipe_id = %(recipe_id)s'''

        query_values = {'recipe_id': recipe_id}

        rows = self.query_data(ingredient_detail_query, query_values)

        if rows is None or len(rows) == 0:
            raise DataNotFound('No rows returned')

        ingredient_details = [{'quantity': ingredient[0],
                               'measure': ingredient[1],
                               'ingredient': ingredient[2],
                               'ingredient_id': ingredient[3],
                               'category': ingredient[4]} for ingredient in rows]

        return ingredient_details

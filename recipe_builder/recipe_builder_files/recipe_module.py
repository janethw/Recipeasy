from flask import render_template
from recipe_files_directory.edamam_class import EdamamRecipes
from recipe_files_directory.recipe_class import Recipe
from app_utils import login_required
import re


class RecipeModule:

    def __init__(self):
        self.recipe_list = None

    # class method creates a class instance
    @classmethod
    def start(cls):
        recipe = cls()
        # start the recipe builder
        recipe.start_recipe()
        return recipe.start_recipe()

    # static method to get inputted ingredients and put them in the edamam recipe search which returns the rendered
    # template and makes sure get_recipe page is protected by login
    @staticmethod
    @login_required
    def get_recipe(ingredients):
        # Edamam_Recipes.edamam_ingredient_search expects a list of ingredients being passed in, we are only
        # interested in URL parameters which are 'ingredient' + a number
        ingredient_list = [ingredients[ingredient] for ingredient in ingredients if ingredients[ingredient] != '' and re.search('^ingredient[0-9]+$', ingredient) is not None]
        try:
            edamam_results = EdamamRecipes.edamam_ingredient_search(ingredient_list)
            return render_template('recipe_search.html',
                                   recipes=edamam_results.output_tabular_data())  # named variable passed in from html
        except Exception as e:
            # if an error has occurred return the error_page with the error message
            return render_template('error_page_inherited.html', error_message=e)

    # static method that gets the recipe details by the recipe ID we've assigned in the database and makes sure
    # recipe details page is protected by login
    @staticmethod
    @login_required
    def get_recipe_details(recipe_id):
        try:
            recipe = Recipe.get_recipe_from_id(recipe_id)
            return render_template('recipe_details.html', recipe=recipe.output_tabular_data(),
                                   ingredients=recipe.get_ingredients(), instructions=recipe.get_instructions())
        except Exception as e:
            return render_template('error_page_inherited.html', error_message=e)

    # rendered the recipe search page, which allows users to enter ingredients to be searched
    @staticmethod
    @login_required
    def start_recipe():
        return render_template('recipe_homepage.html')

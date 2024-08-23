# Recipeasy - Cooking App

## About

Recipeasy is an interactive web-app aimed at engaging children to learn about food and cooking. 
Parents and children can look up recipes based on the ingredients that they have to hand and 
build their food knowledge with the quiz.

## Development Team

Annabel
Elinor 
Eleanor 
Janet
Christabelle 
Clare

## How to run the app

- Install requirements as set out in requirements.txt
- Enter your user credentials for MySQL Workbench into the config.py file. See note in the file about the flask app "secret key".
- Enter your user credentials for Edamam API into the recipe_files_directory/api_congfig.py file.
  * Can be acquired here: https://developer.edamam.com/edamam-docs-recipe-api
- Run Recipeasy_db.sql in MySQL
- Run main.py

### How to perform testing
- Install requirements as set out in requirements.txt
- Make sure main.py is running

#### pytest
- Test files are located in the following directories:

- /login/login_tests
    - test_login_routes.py

- /quiz/tests_quiz
    - test_quiz_module.py
    - test_quiz_routes.py


#### Cypress
- Import the project folder into cypress
- Select end-to-end testing
- Select preferred browser
- Run the recipeasy_testing.js.cy in the browser pop-up
- The tests run automatically

###  Logging
 - Log files will be populated in /logs directory once the app is running 

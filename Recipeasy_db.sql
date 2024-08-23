-- DROP DATABASE Recipeasy;

CREATE DATABASE Recipeasy;

USE Recipeasy;

CREATE TABLE ingredients (
		ingredient_id INTEGER NOT NULL AUTO_INCREMENT,
        ingredient VARCHAR(255),
        category VARCHAR(255),
        PRIMARY KEY (ingredient_id),
        UNIQUE(ingredient)
        );

CREATE TABLE recipe_details (
		recipe_id INTEGER NOT NULL AUTO_INCREMENT,
        uri VARCHAR(384) NOT NULL,
        url VARCHAR(384) NOT NULL,
        image TEXT,
        yield INTEGER,
        title VARCHAR(255) NOT NULL,
        PRIMARY KEY (recipe_id),
        UNIQUE (uri)
        );

CREATE TABLE recipe_ingredients (
		recipe_id INTEGER,
        ingredient_id INTEGER,
		quantity FLOAT,
        measure VARCHAR(255),
        PRIMARY KEY (recipe_id, ingredient_id),
        FOREIGN KEY (recipe_id) REFERENCES recipe_details(recipe_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
        );

CREATE TABLE user_login (
	username VARCHAR(32) NOT NULL UNIQUE,
    email VARCHAR(32) NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    PRIMARY KEY (username)
    );


-- testing credentials for cyrpess tests
INSERT INTO user_login (username, email, password_hash)
VALUES ('eleanor', 'eleanor@test.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
        ('elle', 'elle@test.org', '628e194a914006d2c3f8adc72ecd70325ecae7430a82a32c681eb03281687428'),
	   ('testing', 'tester@testing.com', '05861de03ae99e001c60738f0045b6d2885151fb5b0cca96c23c22b9f1d77802');

CREATE TABLE Questions (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    question_text VARCHAR(255) NOT NULL,
    correct_answer_id INT NOT NULL,
    difficulty INT
);

INSERT INTO Questions (question_text, correct_answer_id, difficulty)
VALUES
('The rice dish ‘paella’ comes from what country?', 2, 1),
('Which fruit is yellow and often found in bunches?', 7, 1),
('What do cows drink to make milk?', 9, 1),
('What is the sweet substance bees make?', 13, 1),
('Which of the following is a vegetable?', 18, 1),
('Which drink comes from cows?', 24, 1),
('What is popcorn made from?', 27, 1),
('What tool do we use to mix ingredients in a bowl?', 29, 1),
('Which ingredient is often used to make cookies sweet?', 35, 1),
('What do we call the process of cooking food in hot oil?', 38, 1),
('What do we call the mixture of flour, eggs, and milk used to make pancakes?', 44, 1),
('Which of these foods is rich in calcium and good for your bones?', 47, 1),
('Which food is a good source of protein that helps build muscles?', 51, 1),
('Which food is rich in vitamin C and helps keep you from getting sick?', 56, 1),
('What should you limit eating to keep your teeth healthy and avoid the dentist?', 57, 1),
('Which country is famous for its spicy food, such as curry?', 61, 1),
('What is the traditional Japanese food made of rice and often served with fish or vegetables?', 66, 1),
('What is the name of the traditional French bread known for its long shape and crispy crust?', 71, 1),
('Foods rich in starch such as pasta and bread are often known by what word starting with the letter C?', 73, 1),
('Which food gives you energy to play and run?', 78, 1),
('What do we call the sweet mixture used to cover cakes and pastries?', 84, 1),
('What is the main ingredient in sushi?', 87, 1),
('What is the traditional Italian dish made of layers of pasta, sauce, and cheese?', 91, 1),
('What is the main ingredient in guacamole?', 93, 1),
('In which country is it common to eat tacos, a dish made with a folded tortilla filled with meat, beans, cheese, and vegetables?', 98, 1),
('What do you call a person who doesn’t eat animal-based food?', 101, 1),
('What vitamin do you get from sunlight?', 108, 1),
('What nutrient comes from egg, meat, and fish?', 110, 1),
('What are dried grapes called?', 115, 1),
('Which food group should you eat the most servings of each day?', 118, 1);

CREATE TABLE Answers (
    choice_id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT,
    choice_text VARCHAR(255) NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

INSERT INTO Answers (question_id, choice_text)
VALUES
(1, 'France'), (1, 'Spain'), (1, 'USA'), (1, 'Japan'),
(2, 'Apple'), (2, 'Orange'), (2, 'Banana'), (2, 'Grape'),
(3, 'Water'), (3, 'Milk'), (3, 'Orange Juice'), (3, 'Squash'),
(4, 'Honey'), (4, 'Chocolate'), (4, 'Jelly'), (4, 'Peanut Butter'),
(5, 'Cake'), (5, 'Carrot'), (5, 'Pasta'), (5, 'Cheese'),
(6, 'Apple Juice'), (6, 'Squash'), (6, 'Lemonade'), (6, 'Milk'),
(7, 'Potatoes'), (7, 'Rice'), (7, 'Corn'), (7, 'Wheat'),
(8, 'Spoon'), (8, 'Knife'), (8, 'Plate'), (8, 'Fork'),
(9, 'Flour'), (9, 'Butter'), (9, 'Sugar'), (9, 'Salt'),
(10, 'Boiling'), (10, 'Frying'), (10, 'Grilling'), (10, 'Steaming'),
(11, 'Gravy'), (11, 'Sauce'), (11, 'Dough'), (11, 'Batter'),
(12, 'Rice'), (12, 'Apples'), (12, 'Cheese'), (12, 'Crisps'),
(13, 'Chips'), (13, 'Donuts'), (13, 'Chicken'), (13, 'Oranges'),
(14, 'Grapes'), (14, 'Cookies'), (14, 'Pizza'), (14, 'Oranges'),
(15, 'Sweets'), (15, 'Fruits'), (15, 'Vegetables'), (15, 'Nuts'),
(16, 'India'), (16, 'Argentina'), (16, 'Nigeria'), (16, 'Germany'),
(17, 'Pizza'), (17, 'Sushi'), (17, 'Tacos'), (17, 'Cottage Pie'),
(18, 'Croissant'), (18, 'Scone'), (18, 'Baguette'), (18, 'Pretzel'),
(19, 'Carbohydrates'), (19, 'Cereal'), (19, 'Carrots'), (19, 'Couscous'),
(20, 'Broccoli'), (20, 'Pasta'), (20, 'Marshmallows'), (20, 'Chocolate'),
(21, 'Batter'), (21, 'Sauce'), (21, 'Gravy'), (21, 'Icing'),
(22, 'Chocolate'), (22, 'Crisps'), (22, 'Rice'), (22, 'Noodles'),
(23, 'Pizza'), (23, 'Spaghetti'), (23, 'Lasagne'), (23, 'Enchiladas'),
(24, 'Avocado'), (24, 'Chickpeas'), (24, 'Onion'), (24, 'Potato'),
(25, 'South Africa'), (25, 'Mexico'), (25, 'Russia'), (25, 'Germany'),
(26, 'Vegan'), (26, 'Carnivore'), (26, 'Vegetarian'), (26, 'Pescatarian'),
(27, 'Vitamin A'), (27, 'Vitamin B'), (27, 'Vitamin C'), (27, 'Vitamin D'),
(28, 'Carbohydrates'), (28, 'Protein'), (28, 'Dairy'), (28, 'Fruits & Vegetables'),
(29, 'Prunes'), (29, 'Dates'), (29, 'Raisins'), (29, 'Apricots'),
(30, 'Dairy'), (30, 'Vegetables'), (30, 'Protein'), (30, 'Carbohydrates');

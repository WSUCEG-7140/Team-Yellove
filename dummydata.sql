-- Insert dummy data into the `categories` table
INSERT INTO categories (name) VALUES
('Appetizers'),
('Salads'),
('Main Courses'),
('Desserts');

-- Insert dummy data into the `items` table
INSERT INTO items (name, description, price, category_id) VALUES
('Mozzarella Sticks', 'Mozzarella cheese sticks, fried to perfection and served with marinara sauce.', 6.99, 1),
('Caesar Salad', 'A classic Caesar salad, made with romaine lettuce, croutons, Parmesan cheese, and a creamy Caesar dressing.', 9.99, 2),
('Hummus and Pita Bread', 'A traditional Middle Eastern dish, made with hummus, pita bread, and vegetables.', 7.99, 1),
('Greek Salad', 'A Greek salad, made with tomatoes, cucumbers, onions, feta cheese, and olives.', 11.99, 2),
('Caprese Salad', 'A Caprese salad, made with fresh mozzarella cheese, tomatoes, and basil.', 10.99, 2),
('Arugula Salad', 'An arugula salad, made with arugula, walnuts, Parmesan cheese, and a balsamic vinaigrette.', 9.99, 2),
('Chicken Parmesan', 'A classic chicken Parmesan, made with breaded chicken, marinara sauce, and mozzarella cheese.', 14.99, 3),
('Steak', 'A grilled steak, served with your choice of sides.', 19.99, 3),
('Salmon', 'A grilled salmon filet, served with your choice of sides.', 17.99, 3),
('Chocolate Lava Cake', 'A warm chocolate lava cake, served with vanilla ice cream.', 7.99, 4),
('Apple Pie', 'A classic apple pie, served with vanilla ice cream.', 6.99, 4),
('Cheesecake', 'A New York-style cheesecake, served with fresh fruit.', 8.99, 4);

-- Insert dummy data into the `ingredients` table
INSERT INTO ingredients (name) VALUES
('Mozzarella Cheese'),
('Tomatoes'),
('Croutons'),
('Parmesan Cheese'),
('Caesar Dressing'),
('Hummus'),
('Pita Bread'),
('Cucumbers'),
('Onions'),
('Feta Cheese'),
('Olives'),
('Chicken'),
('Marinara Sauce'),
('Mozzarella Cheese'),
('Salmon'),
('Vanilla Ice Cream'),
('Apples'),
('Fresh Fruit');

-- Insert dummy data into the `item_ingredients` table
INSERT INTO item_ingredients (item_id, ingredient_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 5),
(2, 6),
(3, 1),
(3, 7),
(4, 8),
(4, 9),
(4, 10),
(5, 1),
(5, 2),
(5, 11),
(6, 12),
(6, 13),
(6, 14),
(7, 15),
(7, 16),
(8, 17),
(8, 18),
(9, 13),
(9, 24);
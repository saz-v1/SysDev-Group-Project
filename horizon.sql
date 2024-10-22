CREATE DATABASE  IF NOT EXISTS `horizon`;
USE horizon;

create table Customer(
Customer_id INT AUTO_INCREMENT PRIMARY KEY,
Full_name  varchar(100) NOT NULL
);

create table staff (
staff_id INT AUTO_INCREMENT PRIMARY KEY,
Full_name varchar(100) NOT NULL,
DOB DATE NOT NULL,
Gender varchar(10),
staff_type ENUM('staff', 'manager', 'admin') DEFAULT 'staff'
);

 

create table accounts (
account_id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT NULL,
staff_id INT NULL,
Email varchar(150),
hashed_password VARCHAR(256) NOT NULL,
FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
FOREIGN KEY(staff_id) REFERENCES staff(staff_id)
);



CREATE TABLE menu (
    menu_id INT AUTO_INCREMENT PRIMARY KEY,
    menu_name VARCHAR(150),
    menu_type ENUM('Main', 'Drink', 'Dessert'),
    price DECIMAL(10, 2)
);

INSERT INTO menu (menu_name, menu_type, price) VALUES
('Deep Dish Pizza', 'Main', 12.99),
('NYC Pizza', 'Main', 11.99),
('Grilled Salmon Fillet', 'Main', 15.99),
('Ribeye Steak', 'Main', 18.99),
('Spaghetti Carbonara', 'Main', 10.99),
('Fish and Chips', 'Main', 11.99),
('Lasagna', 'Main', 13.99),
('Chicken Parmesan', 'Main', 14.99),
('Vegetable Stir Fry', 'Main', 9.99),
('Beef Burger', 'Main', 10.99),
('Gin and Tonic', 'Drink', 6.99),
('Old Fashioned', 'Drink', 8.99),
('Mojito', 'Drink', 7.99),
('Virgin Pina Colada', 'Drink', 5.99),
('Coca-Cola', 'Drink', 2.49),
('Sprite', 'Drink', 2.49),
('Fanta', 'Drink', 2.49),
('Dr Pepper', 'Drink', 2.49),
('Lemonade', 'Drink', 3.49),
('Iced Tea', 'Drink', 3.99),
('Champagne', 'Drink', 25.99),
('White Wine', 'Drink', 15.99),
('Red Wine', 'Drink', 16.99),
('Whiskey', 'Drink', 8.99),
('Vodka', 'Drink', 7.99),
('Rum', 'Drink', 6.99),
('Tequila', 'Drink', 9.99),
('Tiramisu', 'Dessert', 7.99),
('Key Lime Pie', 'Dessert', 6.99),
('Brownie Sundae', 'Dessert', 8.99),
('Cheesecake', 'Dessert', 5.99),
('Ice Cream Sundae', 'Dessert', 6.49);



CREATE TABLE orders(
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    menu_id INT,
    quantity INT,
    new_price DECIMAL(10, 2),
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id)
);


CREATE TABLE restaurant(  
    branch_id int NOT NULL AUTO_INCREMENT,
    restaurant_name VARCHAR(24) NOT NULL,
    restaurant_location VARCHAR(24) NOT NULL,
    restaurant_capacity INT NOT NULL,
    
    PRIMARY KEY(branch_id));
    
INSERT INTO restaurant (restaurant_name, restaurant_location, restaurant_capacity)
VALUES 
    ('The Curry House', 'London', 50),
    ('The Fish Grill', 'Manchester', 30),
    ('The Italian Job', 'Birmingham', 45),
    ('The Crafty Pint', 'Bristol', 70),
    ('Oxford Cafe', 'Oxford', 35),
    ('Cambridge Grill', 'Cambridge', 45),
    ('Liverpool Lounge', 'Liverpool', 50),
    ('Leeds Bistro', 'Leeds', 55),
    ('Newcastle Diner', 'Newcastle', 40),
    ('Cardiff Tavern', 'Cardiff', 60),
    ('Glasgow Grille', 'Glasgow', 65),
    ('Edinburgh Eatery', 'Edinburgh', 55),
    ('Sheffield Bistro', 'Sheffield', 45),
    ('Belfast Bar & Grill', 'Belfast', 50);


CREATE TABLE inventory(  
    inventory_id int NOT NULL AUTO_INCREMENT,
    inventory_name VARCHAR(24) NOT NULL,
    inventory_quantity INT NOT NULL,
    
    PRIMARY KEY(inventory_id));

INSERT INTO inventory (inventory_name, inventory_quantity) VALUES
('Apples', 100),
('Bananas', 150),
('Oranges', 120),
('Carrots', 200),
('Broccoli', 180),
('Tomatoes', 160),
('Chicken', 300),
('Beef', 250),
('Pork', 200),
('Salmon', 180);


CREATE TABLE reservation(  
    reservation_id int NOT NULL AUTO_INCREMENT,
    reservation_date DATETIME NOT NULL,
    reservation_type enum('Standard','Wedding', 'Birthday') DEFAULT 'Standard',
    number_of_guests INT NOT NULL,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    PRIMARY KEY(reservation_id),
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY(branch_id) REFERENCES restaurant(branch_id)
    );

CREATE TABLE receipt(
 receipt_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
 order_id INT NOT NULL,
 FOREIGN KEY(order_id) REFERENCES orders(order_id) 
);

delete from accounts where account_id <19;

select * from accounts;

select * from staff;

select * from customer;

SELECT * FROM restaurant;

show tables;

SELECT 
    r.reservation_id, 
    r.reservation_date, 
    r.reservation_type, 
    r.number_of_guests, 
    c.Full_name AS customer_name, 
    re.restaurant_name, 
    re.restaurant_location
FROM 
    reservation AS r
JOIN 
    Customer AS c ON r.customer_id = c.Customer_id
JOIN 
    restaurant AS re ON r.branch_id = re.branch_id;

SELECT 
    o.order_id,
    m.menu_name,
    m.menu_type,
    m.price,
    o.quantity,
    o.new_price
FROM 
    orders o
JOIN 
    menu m ON o.menu_id = m.menu_id;


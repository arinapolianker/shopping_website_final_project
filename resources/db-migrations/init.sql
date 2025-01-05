DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS favorite_items;


CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_logged BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    item_stock INT NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    shipping_address TEXT NOT NULL,
    item_quantities JSON NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('TEMP', 'CLOSE') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE favorite_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);

INSERT INTO item (name, price, item_stock)
VALUES
    ('Bluetooth Speaker', 49.99, 50),
    ('Portable Mini Speaker', 29.99, 30),
    ('Home Theater Speaker', 200.50, 15),
    ('Waterproof Bluetooth Speaker', 65.70, 25),
    ('Smart Speaker with Voice Assistant', 129.99, 20),
    ('Soundbar with Subwoofer', 249.99, 10),
    ('Outdoor Wireless Speaker', 89.99, 18),
    ('Bookshelf Speakers', 149.99, 12),
    ('Car Audio Speaker System', 119.99, 8),
    ('Party Speaker with LED Lights', 179.99, 10),
    ('Ceiling Mount Speakers', 99.99, 30),
    ('Speaker Stands (Pair)', 39.99, 40),
    ('High-Fidelity Studio Monitor Speaker', 210.30, 10),
    ('Speaker Wall Mount Brackets', 24.99, 60),
    ('Wireless Speaker Charging Dock', 34.99, 35),
    ('WiFi Multi-Room Speaker', 160.50, 15),
    ('Gaming Speaker System', 89.99, 20),
    ('Compact Desktop Speaker', 44.99, 25),
    ('Wireless Earbuds with Speaker', 84.90, 50),
    ('Vintage Style Wooden Speaker', 99.99, 10);



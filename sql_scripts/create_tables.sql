DROP TABLE IF EXISTS order_payment_details;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS product_order;
DROP TABLE IF EXISTS order_cart;
DROP TABLE IF EXISTS delivery;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS registered_user;
DROP TABLE IF EXISTS payment_detail;
DROP TABLE IF EXISTS product_sub_category;
DROP TABLE IF EXISTS sub_category;
DROP TABLE IF EXISTS super_category;
DROP TABLE IF EXISTS product_variant_option;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS product_variant;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS discount;

CREATE TABLE discount(
    id INT NOT NULL AUTO_INCREMENT,
    description VARCHAR(20),
    discount_amount NUMERIC(6, 2),
    status VARCHAR(8),
    PRIMARY KEY(ID)
);
CREATE TABLE product (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    description TEXT(100000),
    base_price NUMERIC(10, 2),
    discount_id INT,
    brand VARCHAR(50),
    PRIMARY KEY (id),
    FOREIGN KEY (discount_id) REFERENCES discount(id) ON DELETE
    SET NULL
);
CREATE TABLE product_variant (
    sku CHAR(8),
    name VARCHAR(50),
    product_id INT NOT NULL,
    price NUMERIC(10, 2),
    image_url VARCHAR(255),
    PRIMARY KEY (sku),
    FOREIGN key (product_id) REFERENCES product(id) ON DELETE CASCADE
);
CREATE TABLE options (
    option_id INT NOT NULL AUTO_INCREMENT,
    prod_description TEXT(100000),
    price_diff NUMERIC(10, 2) CHECK (price_diff > 0),
    PRIMARY KEY (option_id)
);
CREATE TABLE product_variant_option (
    id INT NOT NULL AUTO_INCREMENT,
    sku CHAR(8),
    option_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (sku) REFERENCES product_variant(sku) ON DELETE CASCADE,
    FOREIGN key (option_id) REFERENCES options(option_id) ON DELETE CASCADE
);
CREATE TABLE super_category (
    id INT NOT NULL AUTO_INCREMENT,
    cat_name VARCHAR(100),
    PRIMARY KEY (id)
);
CREATE TABLE sub_category(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20),
    description TEXT(10000),
    super_category_id VARCHAR(20),
    FOREIGN KEY(id) REFERENCES super_category(id) ON DELETE CASCADE on update cascade
);
CREATE TABLE product_sub_category (
    id INT NOT NULL AUTO_INCREMENT,
    product_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    FOREIGN key (subcategory_id) REFERENCES sub_category(id) ON DELETE CASCADE
);
CREATE TABLE payment_detail (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    card_no VARCHAR(20) NOT NULL,
    provider VARCHAR(20)
);
CREATE TABLE registered_user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(512) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(512),
    mobile_no VARCHAR(10),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_detail_id INT,
    is_admin BOOL,
    FOREIGN KEY (payment_detail_id) REFERENCES payment_detail(id) ON DELETE
    SET NULL
);
CREATE TABLE user(
	ID INT NOT NULL AUTO_INCREMENT,
	is_guest BOOL,
    registered_user_id INT,
    PRIMARY KEY(ID),
    FOREIGN KEY(registered_user_id) REFERENCES registered_user(ID)
		ON DELETE SET NULL
);
CREATE TABLE location(
	ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    is_main_city BOOL,
    delivery_cost NUMERIC(10,2) CHECK(delivery_cost>0),
    PRIMARY KEY (ID)
);
CREATE TABLE delivery(
	ID INT NOT NULL AUTO_INCREMENT,
    delivery_method VARCHAR(20),
    provider VARCHAR(20),
    location_id INT ,
    PRIMARY KEY (ID),
    FOREIGN KEY (location_id) REFERENCES location(ID)
		ON DELETE SET NULL
);

CREATE TABLE order_cart (
    order_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    billing_date DATE,
    is_billed BOOL,
    delivery_id INT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (delivery_id) REFERENCES delivery(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE product_order(
    id INT NOT NULL AUTO_INCREMENT,
    sku VARCHAR(20),
    order_id INT,
    price NUMERIC(10, 2) NOT NULL,
    quantity INT,
    PRIMARY KEY(id),
    FOREIGN KEY(order_id) REFERENCES order_cart(order_id) ON DELETE CASCADE on update cascade,
    FOREIGN KEY(sku) REFERENCES product_variant(sku) ON DELETE CASCADE on update cascade
);

CREATE TABLE inventory(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    quantity INT,
    sku VARCHAR(20),
    FOREIGN KEY(sku) REFERENCES product_variant(sku)
);

CREATE TABLE order_payment_details(
	ID INT NOT NULL AUTO_INCREMENT,
    order_id INT ,
    cardnumber VARCHAR(16),
    provider VARCHAR(20),
    PRIMARY KEY (ID),
    FOREIGN KEY (order_id) REFERENCES order_cart(order_id)
		ON DELETE SET NULL
);

DELIMITER $$
CREATE PROCEDURE create_user(IN field_dict JSON)
BEGIN
    
    DECLARE registered_user_id INT;
    DECLARE payment_detail_id INT;

    INSERT INTO registered_user (username, password, firstname, lastname, email, address, mobile_no, is_admin, created_date, payment_detail_id) 
    VALUES (field_dict->>'$.username', field_dict->>'$.password', field_dict->>'$.firstname', field_dict->>'$.lastname', field_dict->>'$.email', field_dict->>'$.address', field_dict->>'$.mobile_no', 0, NOW(), NULL);
    SET registered_user_id = LAST_INSERT_ID();
    
    INSERT INTO user (is_guest, registered_user_id) 
    VALUES (0, registered_user_id);
    
    INSERT INTO payment_detail (card_no, provider) 
    VALUES (field_dict->>'$.card_no', field_dict->>'$.provider');
    SET payment_detail_id = LAST_INSERT_ID();
    
    UPDATE registered_user SET payment_detail_id = payment_detail_id WHERE id = registered_user_id;

END$$
DELIMITER ;
CREATE TABLE discount(
    id INT NOT NULL AUTO_INCREMENT,
    description VARCHAR(20),
    discount_amount NUMERIC(6, 2),
    status VARCHAR(8),
    PRIMARY KEY(id)
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
CREATE TABLE product_option (
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
    FOREIGN key (option_id) REFERENCES product_option(option_id) ON DELETE CASCADE
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
    sub_category_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    FOREIGN key (sub_category_id) REFERENCES sub_category(id) ON DELETE CASCADE
);
CREATE TABLE payment_detail (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    card_no VARCHAR(20) NOT NULL,
    provider VARCHAR(20)
);
CREATE TABLE registered_user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(512) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(512),
    mobile_no VARCHAR(10),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_detail_id INT,
    FOREIGN KEY (payment_detail_id) REFERENCES payment_detail(id) ON DELETE
    SET NULL
);
CREATE TABLE user(
	id INT NOT NULL AUTO_INCREMENT,
	is_guest BOOL,
    registered_user_id INT,
    PRIMARY KEY(id),
    FOREIGN KEY(registered_user_id) REFERENCES registered_user(id)
		ON DELETE SET NULL
);
CREATE TABLE location(
	id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    is_main_city BOOL,
    delivery_cost NUMERIC(10,2) CHECK(delivery_cost>0),
    PRIMARY KEY (id)
);
CREATE TABLE delivery(
	id INT NOT NULL AUTO_INCREMENT,
    delivery_method VARCHAR(20),
    provider VARCHAR(20),
    location_id INT ,
    PRIMARY KEY (id),
    FOREIGN KEY (location_id) REFERENCES location(id)
		ON DELETE SET NULL
);

CREATE TABLE order_cart (
    order_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    billing_date DATE,
    is_billed BOOL,
    delivery_id INT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (user_id) REFERENCES USER(id),
    FOREIGN KEY (delivery_id) REFERENCES DELIVERY(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE product_order(
    id INT NOT NULL AUTO_INCREMENT,
    sku VARCHAR(20),
    order_id INT,
    price NUMERIC(10, 2) NOT NULL,
    quantity INT,
    PRIMARY KEY(id),
    FOREIGN KEY(order_id) REFERENCES order_cart(order_id) ON DELETE CASCADE on update cascade
);
CREATE TABLE inventory(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    quantity INT,
    sku VARCHAR(20),
    FOREIGN KEY(sku) REFERENCES product_variant(sku)
);

CREATE TABLE order_payment_details(
	id INT NOT NULL AUTO_INCREMENT,
    order_id INT ,
    card_no VARCHAR(16),
    provider VARCHAR(20),
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES order_cart(order_id)
		ON DELETE SET NULL
);

INSERT INTO discount(description, discount_amount, status) VALUES ('Christmas', 2000.00, 'Pending');
INSERT INTO product(name, description, base_price, discount_id, brand) 
VALUES ('Teddy bear', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
1000.00, 1, 'Foo Toys');
INSERT INTO product_variant 
VALUES ('ABCD1234', 'Brown Teddy bear', 1, 1000.00, NULL); 
INSERT INTO product_option(prod_description, price_diff) 
VALUES ('Sample description', 100.00);
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1234', 1); 
INSERT INTO super_category(cat_name)
VALUES ('Toys'); 
INSERT INTO sub_category(name, description, super_category_id) 
VALUES ('Soft Toys', 'Sample description', 1); 
INSERT INTO product_sub_category(product_id, sub_category_id) 
VALUES (1, 1); 
INSERT INTO payment_detail(card_no, provider) 
VALUES ('1234567812345678', 'Visa');
INSERT INTO registered_user(user_name, password, first_name, last_name, email, address, mobile_no, payment_detail_id) 
VALUES ('thulasithang', '4d27eae655e7272b21c5b0a539656a8ae869d75f', 'Thulasithan', 'Gnanenthiram', 'thulasithang@sample.com', 'T56: Bayawechcha paara, anda yata', '0112729729', 1);  
INSERT INTO user(is_guest, registered_user_id) 
VALUES (FALSE, 1);  
INSERT INTO location(name, is_main_city, delivery_cost) 
VALUES ('Colombo', TRUE, 100.00);  
INSERT INTO delivery(delivery_method, provider, location_id) 
VALUES ('Courier', 'DHL', 1);  
INSERT INTO order_cart(user_id, billing_date, is_billed, delivery_id) 
VALUES (1, '2022-02-14', TRUE, 1);  
INSERT INTO product_order(sku, order_id, price, quantity) 
VALUES ('ABCD1234', 1, 1500.00, 1);
INSERT INTO inventory(quantity, sku) 
VALUES (10, 'ABCD1234');  
INSERT INTO order_payment_details(order_id, card_no, provider) 
VALUES (1, '1234567812345678', 'Visa');

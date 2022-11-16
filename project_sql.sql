CREATE TABLE product_variant
	(sku			CHAR(8), 
	 name			VARCHAR(50),
	 product_id		INT(7) NOT NULL,
	 price			NUMERIC(10,2),
	 image_url		VARCHAR(255),
	 PRIMARY KEY (sku),
	 FOREIGN key (product_id) REFERENCES product(id)
		ON DELETE CASCADE
	);

CREATE TABLE product_variant_option
	(id			    INT(7) NOT NULL AUTO_INCREMENT, 
	 sku			CHAR(8),
	 option_id	    INT(7) NOT NULL, 
	 PRIMARY KEY (id),
	 FOREIGN KEY (sku) REFERENCES product_variant(sku)
		ON DELETE CASCADE,
	 FOREIGN key (option_id) REFERENCES options(option_id)
		ON DELETE CASCADE
	);

CREATE TABLE product
	(id			    INT(7) NOT NULL AUTO_INCREMENT, 
	 name			VARCHAR(50),
	 description	VARCHAR(100), 
     base_price		NUMERIC(10,2),
     discount_id	INT(7) NOT NULL,
	 brand		    VARCHAR(50), 
	 PRIMARY KEY (id),
	 FOREIGN KEY (discount_id) REFERENCES discount(id)
		ON DELETE SET NULL
	);

CREATE TABLE product_sub_category
	(id			    INT(7) NOT NULL AUTO_INCREMENT, 
	 product_id	    INT(7) NOT NULL, 
	 subcategory_id INT(7) NOT NULL, 
	 PRIMARY KEY (id),
	 FOREIGN KEY (product_id) REFERENCES product(id)
		ON DELETE CASCADE,
	 FOREIGN key (subcategory_id) REFERENCES sub_category(id)
		ON DELETE CASCADE
	);
CREATE TABLE payment_detail (
    id INT(7) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    card_no VARCHAR(20) NOT NULL,
    provider VARCHAR(20)
);

CREATE TABLE registered_user (
    id INT(7) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(512) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(512),
    mobile_no VARCHAR(10),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_detail_id INT(7),
    FOREIGN KEY (payment_detail_id) REFERENCES payment_detail(id)
        ON DELETE SET NULL
);

CREATE TABLE options
	(option_id		    INT(7) NOT NULL AUTO_INCREMENT, 
	 prod_description	TEXT(100000), 
	 price_diff		    NUMERIC(10, 2) CHECK (price_diff > 0),
	 PRIMARY KEY (option_id)
	);

CREATE TABLE super_catogory
	(super_catogory_id	INT(7) NOT NULL AUTO_INCREMENT, 
	 cat_name       	VARCHAR(100), 
	 price_diff		    NUMERIC(10, 2) CHECK (price_diff > 0),
	 PRIMARY KEY (super_catogory_id)
	);

CREATE TABLE order_cart
    (order_id       INT(7) NOT NULL AUTO_INCREMENT,
     user_id        INT(7) NOT NULL,
     billing_date   DATE,
     is_billed      BOOL,
     delivery_id    INT(7),
     PRIMARY KEY (order_id),
     FOREIGN KEY (user_id) REFERENCES USER(id),
     FOREIGN KEY (delivery_id) REFERENCES DELIVERY(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );

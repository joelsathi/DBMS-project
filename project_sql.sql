CREATE TABLE product_variant
	(sku			CHAR(8), 
	 name			VARCHAR(50),
	 inventory_id	INT(7) NOT NULL AUTO_INCREMENT, 
	 product_id		INT(7) NOT NULL AUTO_INCREMENT,
	 price			NUMERIC(10,2),
	 image_url		VARCHAR(255),
	 PRIMARY KEY (sku),
	 FOREIGN KEY (inventory_id) REFERENCES inventory(id)
		ON DELETE CASCADE,
	 FOREIGN key (product_id) REFERENCES product(id)
		ON DELETE SET NULL
	);

CREATE TABLE product_variant_option
	(id			    INT(7) NOT NULL AUTO_INCREMENT, 
	 sku			CHAR(8),
	 option_id	    INT(7) NOT NULL AUTO_INCREMENT, 
	 PRIMARY KEY (id),
	 FOREIGN KEY (sku) REFERENCES product_variant(sku)
		ON DELETE SET NULL,
	 FOREIGN key (option_id) REFERENCES options(option_id)
		ON DELETE SET NULL
	);

CREATE TABLE product
	(id			    INT(7) NOT NULL AUTO_INCREMENT, 
	 name			VARCHAR(50),
	 description	VARCHAR(100), 
     base_price		NUMERIC(10,2),
     discount_id	INT(7) NOT NULL AUTO_INCREMENT,
	 brand		    VARCHAR(50), 
	 PRIMARY KEY (id),
	 FOREIGN KEY (discount_id) REFERENCES discount(id)
		ON DELETE CASCADE
	);

CREATE TABLE product_sub_category
	(id			    INT(7) NOT NULL AUTO_INCREMENT, 
	 product_id	    INT(7) NOT NULL AUTO_INCREMENT, 
	 subcategory_id INT(7) NOT NULL AUTO_INCREMENT, 
	 PRIMARY KEY (id),
	 FOREIGN KEY (product_id) REFERENCES product(id)
		ON DELETE SET NULL,
	 FOREIGN key (subcategory_id) REFERENCES sub_category(id)
		ON DELETE SET NULL
	);

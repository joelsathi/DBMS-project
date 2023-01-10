INSERT INTO discount(description, discount_amount, status) VALUES ('Christmas', 2000.00, 'Pending');
INSERT INTO product(name, description, base_price, discount_id, brand) 
VALUES ('Teddy bear', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
1000.00, 1, 'Foo Toys');
INSERT INTO product(name, description, base_price, discount_id, brand) 
VALUES ('Iphone 14 Pro Max', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
200000.00, 1, 'Apple');
INSERT INTO product_variant 
VALUES ('ABCD1234', 'Brown Teddy bear', 1, 1000.00, 'https://www.buildabear.co.uk/dw/image/v2/BBNG_PRD/on/demandware.static/-/Sites-buildabear-master/default/dw2b81d8a7/28502x.jpg?sw=600&sh=600&sm=fit&q=70'); 
INSERT INTO product_variant VALUES ('ABCD1235', 'Iphone 14 Pro Max green 64GB',2, 200000, 'https://celltronics.lk/wp-content/uploads/2022/09/Apple-iPhone-14-Pro-Max-2.jpg'); 
INSERT INTO options(prod_description, price_diff) 
VALUES ('Sample description', 100.00);
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1234', 1); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1235', 1); 
INSERT INTO super_category(cat_name)
VALUES ('Toys'); 
INSERT INTO super_category(cat_name)
VALUES ('Electronics');
INSERT INTO sub_category(name, description, super_category_id) 
VALUES ('Soft Toys', 'Sample description', 1); 
INSERT INTO sub_category(name, description, super_category_id) 
VALUES ('Mobile Phones', 'Sample description', 2); 
INSERT INTO product_sub_category(product_id, subcategory_id) 
VALUES (1, 1); 
INSERT INTO product_sub_category(product_id, subcategory_id) 
VALUES (2, 2);
INSERT INTO payment_detail(card_no, provider) 
VALUES ('1234567812345678', 'Visa');
INSERT INTO registered_user(username, password, firstname, lastname, email, address, mobile_no, payment_detail_id) 
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
INSERT INTO inventory(quantity, sku) 
VALUES (5, 'ABCD1235'); 
INSERT INTO order_payment_details(order_id, cardnumber, provider) 
VALUES (1, '1234567812345678', 'Visa');
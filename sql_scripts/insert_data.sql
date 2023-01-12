INSERT INTO discount(description, discount_amount, status) VALUES ('Christmas', 2000.00, 'Pending');

INSERT INTO product(name, description, base_price, discount_id, brand, image_url) 
VALUES ('Teddy bear', 'Cute teddy bear Gray small',
1000.00, 1, 'Foo Toys', 'https://m.media-amazon.com/images/I/71H6DfoO1JL._AC_SL1500_.jpg');
INSERT INTO product(name, description, base_price, discount_id, brand, image_url) 
VALUES ('Iphone 14 Pro Max', 'Base model with 32GB black',
200000.00, 1, 'Apple', 'https://www.istore.co.za/media/catalog/product/i/p/iphone_14_pro_max_deep_purple-6_1.jpg?optimize=medium&bg-color=255,255,255&fit=bounds&height=700&width=700&canvas=700:700');

INSERT INTO product_variant 
VALUES ('ABCD1234', 'Teddy bear brown medium', 1, 1400.00, 'https://m.media-amazon.com/images/I/7168qr79CzL._AC_SL1500_.jpg'); 
INSERT INTO product_variant 
VALUES ('ABCD1235', 'Teddy bear white medium', 1, 1500.00, 'https://m.media-amazon.com/images/I/81+gjph2J8L._AC_SL1500_.jpg'); 
INSERT INTO product_variant 
VALUES ('ABCD1236', 'Teddy bear brown large', 1, 2100.00, 'https://cdn11.bigcommerce.com/s-dee9d/images/stencil/1280x1280/products/114/11500/123__16913.1661790668.jpg?c=2'); 
INSERT INTO product_variant 
VALUES ('ABCD1237', 'Teddy bear white large', 1, 2200.00, 'https://cdn11.bigcommerce.com/s-dee9d/images/stencil/1280x1280/products/114/11500/123__16913.1661790668.jpg?c=2'); 

INSERT INTO product_variant 
VALUES ('ABCD1240', 'Iphone 14 Pro Max green 64GB',2, 220000, 'https://static-01.daraz.lk/p/0fc14d98b79a9e04b24c8131fcae1cca.jpg'); 

INSERT INTO options(prod_description, price_diff) 
VALUES ('Teddy bear color brown', 100.00);
INSERT INTO options(prod_description, price_diff) 
VALUES ('Teddy bear color white', 200.00);
INSERT INTO options(prod_description, price_diff) 
VALUES ('Teddy bear size medium', 300.00);
INSERT INTO options(prod_description, price_diff) 
VALUES ('Teddy bear size large', 1000.00);

INSERT INTO options(prod_description, price_diff) 
VALUES ('Iphone 14 Pro Max size 64GB', 10000.00);
INSERT INTO options(prod_description, price_diff) 
VALUES ('Iphone 14 Pro Max size 128GB', 10000.00);
INSERT INTO options(prod_description, price_diff) 
VALUES ('Iphone 14 Pro Max color green', 10000.00);
INSERT INTO options(prod_description, price_diff) 
VALUES ('Iphone 14 Pro Max size red', 10000.00);


INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1234', 1); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1234', 3); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1235', 2); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1235', 3); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1236', 1); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1236', 4); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1237', 2); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1237', 4); 

INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1240', 5); 
INSERT INTO product_variant_option(sku, option_id) 
VALUES ('ABCD1240', 7); 

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
INSERT INTO registered_user(username, password, firstname, lastname, email, address, mobile_no, payment_detail_id, is_admin) 
VALUES ('thulasithang', '4d27eae655e7272b21c5b0a539656a8ae869d75f', 'Thulasithan', 'Gnanenthiram', 'thulasithang@sample.com', 'T56: Bayawechcha paara, anda yata', '0112729729', 1, TRUE);  
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
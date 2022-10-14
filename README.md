# DBMS-project

Single Vendor E-Commerce Platform <br>

C is a local chain retailer in Texas. Over the years, they were able to acquire a significant
customer base mainly by providing an efficient and reliable service. With Amazon becoming a
threat to almost every retailer nationwide, C is now considering to reach the technology side
as an effort of keeping up with the competition. C is family owned and currently run by the
brothers. They see the lack of online presence is a major issue with C in comparison to
Amazon. In order to overcome this, C has decided to hire a team of experts to analyse and
design a e-commerce platform for the store. The company maintains own stock in several
warehouses and already has a courier service subsidiary which takes care of delivery
functions. The target of the company is to have a better visibility within Texas. In the initial
phase C is considering to populate the platform with only a subset of all the commodities in
offered in the retailer. Given that there are over 10,000 different products currently offered in
their stores, the company decided to only offer consumer electronics and toys in the first
phase.
<br>

<p>
As per the requirement, system must first hold details about different products. Each product
has at least one variant. A variant defines a specific variety of a product. For an example,
iPhone X is the product while 16GB and 32GB are product variants. Also colors Black and
Red are too variants for the iPhone. Depending on the variant, the price of the product vary.
If the product has no varieties, it will have the default variant which will contain the price of it.
Moreover each product will have a SKU assigned by the warehouse. Each product belongs to
one or more categories. The product catalog of the system would use categories for search
and sort the products for the user. Some categories are Mobile, Speakers, etc. Each category
can also have sub categories. While there are few common attributes of products, such as
title, sku, weight etc. each product need the freedom to define its own custom attributes. Since
the system supports online purchase of the products, the inventory of the products need to be
managed by the system as well. Inventory would essentially maintain a count of the availability
from each product variant. To simply the initial design, consider that all products are stored
only in one warehouse. When a customer browse the platform, he/she could either register
with the platform or browse as a guest. Customer could add products to the cart without
completing any purchase. When product selection is done, he/she could checkout the cart. At
this moment the cart turns to an order and the cart is emptied. Every order should contain the
customer contact detail in extent (for logged in users, this can be taken from their already
provided information). Apart from that, delivery method (store pickup, delivery) and payment
method (cash on delivery or card) must be specified. Once a checkout is completed, the
inventory must reflect the changes. Consistency in transactions (inventory counts) must be
considered when validating purchases.
</p>

Apart from these C, requires a comprehensive report system for monitoring and analytics of
the platform. The reports include:
<br>
<li> Quarterly sales report for a given year </li>
<li> Products with most number of sales in a given period </li>
<li> Product category with most orders </li>
<li> Given a product, time period with most interest to it </li>
<li> Customer </li>
<li> order report </li>
<br>

Additionally, a delivery module needs to be created which shows the approximate delivery
times for a given product. The rules for the module are a follows 
<br>
<li> If product has stock, delivery is to a main city (ex: Colombo), it’s 5 days </li>
<li> If product has stock, but delivery is not to a main city (ex: Negombo), it’s 7 days </li>
<li> If product has no stock add 3 days each of the above cases </li>
<li> Delivery estimate should appear in order when it’s in checkout
</li>
<br>

These information need to be states with the product and with the order when checking out.
<br>

As experts of database design, you are hired first analyse the requirement and propose a
database design to encapsulate all the above functionalities. In order to test the functioning
of the database, a simple UI is required.
<br>

# Task
Your task is to model the database design to encapsulate these requirement. It should
consider all entities and relationships given in the description. Moreover you need to identify
the places where procedures, functions and triggers can be employed to guarantee ACID
properties. Foreign keys and primary keys must be set to maintain consistency. Indexing
should be done when necessary.
<br>
<br>
Additionally, the you must get a domain idea by reading related material and take assumptions
when not explicitly provided. The database must be populated with at least 40 products, with
variants and at least 10 different categories. These data insertions can be done manually and
no need of UI components just for the task of data input. 

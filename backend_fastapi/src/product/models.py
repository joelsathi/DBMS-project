from ..core import model, field

class ProductModel(model.BaseDBModel):
    __tablename__ = "product"

    id = field.IntegerDBField(is_primary_key=True)
    name = field.CharDBField(max_length=50)
    description = field.TextDBField()
    base_price = field.FloatDBField()
    brand = field.CharDBField(max_length=50)

    discount_id = None      # TODO foriengn key

    def serialize(self):
        fields = [
            "id",
            "name",
            "description",
            "base_price",
            "brand",
        ]

        return {f: getattr(self, f) for f in fields}

class ProductVariantModel(model.BaseDBModel):
    __tablename__ = "product_variant"

    sku = field.CharDBField(max_length=8, is_primary_key=True)
    name = field.CharDBField(max_length=50)
    price = field.FloatDBField()
    image_url = field.CharDBField(max_length=255)

    product_id = None      # TODO foriengn key

    def serialize(self):
        fields = [
            "sku",
            "name",
            "price",
            "image_url",
        ]

        return {f: getattr(self, f) for f in fields}
    
class SubCategoryModel(model.BaseDBModel):
    __tablename__ = "sub_category"

    id = field.IntegerDBField(is_primary_key=True)
    name = field.CharDBField(max_length=20)
    description = field.TextDBField()

    super_category_id = None      # TODO foriengn key

    def serialize(self):
        fields = [
            "id",
            "name",
            "description",
        ]

        return {f: getattr(self, f) for f in fields}

class SuperCategoryModel(model.BaseDBModel):
    __tablename__ = "super_category"

    id = field.IntegerDBField(is_primary_key=True)
    cat_name = field.CharDBField(max_length=100)

    def serialize(self):
        fields = [
            "id",
            "cat_name",
        ]

        return {f: getattr(self, f) for f in fields}

class DiscountModel(model.BaseDBModel):
    __tablename__ = "discount"

    id = field.IntegerDBField(is_primary_key=True)
    description = field.CharDBField(max_length=20)
    discount_amount = field.FloatDBField()
    status = field.CharDBField(max_length=8)

    def serialize(self):
        fields = [
            "id",
            "description",
            "discount_amount",
            "status",
        ]

        return {f: getattr(self, f) for f in fields}

class OptionsModel(model.BaseDBModel):
    __tablename__ = "options"

    option_id = field.IntegerDBField(is_primary_key=True)
    prod_description = field.TextDBField()
    price_diff = field.FloatDBField()

    def serialize(self):
        fields = [
            "option_id",
            "prod_description",
            "price_diff",
        ]

        return {f: getattr(self, f) for f in fields}

class InventoryModel(model.BaseDBModel):
    __tablename__ = "inventory"

    id = field.IntegerDBField(is_primary_key=True)
    quantity = field.IntegerDBField()

    # sku = field.CharDBField(max_length=20)

    sku = None          # TODO foreign key

    def serialize(self):
        fields = [
            "id",
            "quantity",
        ]

        return {f: getattr(self, f) for f in fields}

class ProductSubCategoryModel(model.BaseDBModel):
    __tablename__ = "product_sub_category"

    id = field.IntegerDBField(is_primary_key=True)

    product_id = None           # TODO foreign key
    subcategory_id = None       # TODO foreign key

    def serialize(self):
        fields = [
            "id",
        ]

        return {f: getattr(self, f) for f in fields}

class ProductVarientOptionsModel(model.BaseDBModel):
    __tablename__ = "product_variant_option"

    id = field.IntegerDBField(is_primary_key=True)

    # sku = field.CharDBField(max_length=8) 
    # option_id = field.IntegerDBField()  

    sku = None           # TODO foreign key
    option_id = None       # TODO foreign key

    def serialize(self):
        fields = [
            "id",
        ]

        return {f: getattr(self, f) for f in fields}
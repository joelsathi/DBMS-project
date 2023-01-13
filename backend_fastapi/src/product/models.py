from ..core import model, field


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


class ProductModel(model.BaseDBModel):
    __tablename__ = "product"

    id = field.IntegerDBField(is_primary_key=True)
    name = field.CharDBField(max_length=50)
    description = field.TextDBField()
    base_price = field.FloatDBField()
    brand = field.CharDBField(max_length=50)
    image_url = field.CharDBField(max_length=255)

    discount_id = field.ForeignKeyDBField(related_model=DiscountModel, allow_null=True)

    def serialize(self):
        fields = [
            "id",
            "name",
            "description",
            "base_price",
            "brand",
            "image_url",
            "discount_id",
        ]

        return {f: getattr(self, f) for f in fields}


class ProductVariantModel(model.BaseDBModel):
    __tablename__ = "product_variant"

    sku = field.CharDBField(max_length=8, is_primary_key=True)
    name = field.CharDBField(max_length=50)
    price = field.FloatDBField()
    image_url = field.CharDBField(max_length=255)

    product_id = field.ForeignKeyDBField(related_model=ProductModel, allow_null=False)

    def serialize(self):
        fields = [
            "sku",
            "name",
            "price",
            "image_url",
            "product_id",
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


class SubCategoryModel(model.BaseDBModel):
    __tablename__ = "sub_category"

    id = field.IntegerDBField(is_primary_key=True)
    name = field.CharDBField(max_length=20)
    description = field.TextDBField()

    super_category_id = field.ForeignKeyDBField(
        related_model=SuperCategoryModel, allow_null=False
    )

    def serialize(self):
        fields = ["id", "name", "description", "super_category_id"]

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

    sku = field.ForeignKeyDBField(related_model=ProductVariantModel, allow_null=False)

    def serialize(self):
        fields = [
            "id",
            "quantity",
            "sku",
        ]

        return {f: getattr(self, f) for f in fields}


class ProductSubCategoryModel(model.BaseDBModel):
    __tablename__ = "product_sub_category"

    id = field.IntegerDBField(is_primary_key=True)

    product_id = field.ForeignKeyDBField(related_model=ProductModel, allow_null=False)
    subcategory_id = field.ForeignKeyDBField(
        related_model=SubCategoryModel, allow_null=False
    )

    def serialize(self):
        fields = [
            "id",
            "product_id",
            "subcategory_id",
        ]

        return {f: getattr(self, f) for f in fields}


class ProductVarientOptionsModel(model.BaseDBModel):
    __tablename__ = "product_variant_option"

    id = field.IntegerDBField(is_primary_key=True)

    # sku = field.CharDBField(max_length=8)
    # option_id = field.IntegerDBField()

    sku = field.ForeignKeyDBField(related_model=ProductVariantModel, allow_null=False)
    option_id = field.ForeignKeyDBField(related_model=OptionsModel, allow_null=False)

    def serialize(self):
        fields = [
            "id",
            "sku",
            "option_id",
        ]

        return {f: getattr(self, f) for f in fields}

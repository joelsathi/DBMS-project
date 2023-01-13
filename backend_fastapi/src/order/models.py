from ..core import model, field

from ..auth.models import UserDBModel
from ..product.models import ProductVariantModel


class LocationModel(model.BaseDBModel):
    __tablename__ = "location"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    name = field.CharDBField(max_length=20)
    is_main_city = field.BooleanDBField()
    delivery_cost = field.FloatDBField()

    def serialize(self):
        fields = [
            "id",
            "name",
            "is_main_city",
            "delivery_cost",
        ]

        return {f: getattr(self, f) for f in fields}


class DeliveryModel(model.BaseDBModel):
    __tablename__ = "delivery"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    delivery_method = field.CharDBField(max_length=20)
    provider = field.CharDBField(max_length=20)

    location_id = field.ForeignKeyDBField(related_model=LocationModel, allow_null=True)

    def serialize(self):
        fields = [
            "id",
            "delivery_method",
            "provider",
            "location_id",
        ]

        return {f: getattr(self, f) for f in fields}


class OrderCartModel(model.BaseDBModel):
    __tablename__ = "order_cart"

    order_id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    billing_date = field.DateTimeDBField(datetime_format="%Y-%m-%d %H:%M:%S")
    is_billed = field.BaseDBField()

    user_id = field.ForeignKeyDBField(related_model=UserDBModel, allow_null=False)
    delivery_id = field.ForeignKeyDBField(related_model=DeliveryModel, allow_null=True)

    def serialize(self):
        fields = [
            "order_id",
            "is_billed",
            "user_id",
            "delivery_id",
        ]

        return {f: getattr(self, f) for f in fields}


class ProductOrderModel(model.BaseDBModel):
    __tablename__ = "product_order"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    price = field.FloatDBField()
    quantity = field.IntegerDBField()

    sku = field.ForeignKeyDBField(related_model=ProductVariantModel, allow_null=False)
    order_id = field.ForeignKeyDBField(related_model=OrderCartModel, allow_null=False)

    def serialize(self):
        fields = [
            "id",
            "price",
            "quantity",
            "sku",
            "order_id",
        ]

        return {f: getattr(self, f) for f in fields}


class OrderPaymentDetailModel(model.BaseDBModel):
    __tablename__ = "order_payment_details"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    cardnumber = field.CharDBField(max_length=16)
    provider = field.CharDBField(max_length=20)

    order_id = field.ForeignKeyDBField(related_model=OrderCartModel, allow_null=False)

    def serialize(self):
        fields = [
            "id",
            "cardnumber",
            "provider",
            "order_id",
        ]

        return {f: getattr(self, f) for f in fields}

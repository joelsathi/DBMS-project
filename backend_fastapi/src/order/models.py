from ..core import model, field


class OrderCartModel(model.BaseDBModel):
    __tablename__ = "order_cart"

    order_id = field.IntegerDBField(is_primary_key=True)
    billing_date = None  # TODO
    is_billed = field.BaseDBField()

    user_id = None  # TODO foriengn key
    delivery_id = None  # TODO foriengn key

    def serialize(self):
        fields = [
            "order_id",
            "is_billed",
        ]

        return {f: getattr(self, f) for f in fields}


class ProductOrderModel(model.BaseDBModel):
    __tablename__ = "product_order"

    id = field.IntegerDBField(is_primary_key=True)
    price = field.FloatDBField()
    quantity = field.IntegerDBField()

    sku = None  # TODO have to consider the ER again and decide
    order_id = None  # TODO foriengn key

    def serialize(self):
        fields = [
            "id",
            "price",
            "quantity",
        ]

        return {f: getattr(self, f) for f in fields}


class OrderPaymentDetailModel(model.BaseDBModel):
    __tablename__ = "order_payment_details"

    ID = field.IntegerDBField(is_primary_key=True)
    cardnumber = field.CharDBField(max_length=16)
    provider = field.CharDBField(max_length=20)

    order_id = None  # TODO foriengn key

    def serialize(self):
        fields = [
            "ID",
            "cardnumber",
            "provider",
        ]

        return {f: getattr(self, f) for f in fields}


class DeliveryModel(model.BaseDBModel):
    __tablename__ = "delivery"

    ID = field.IntegerDBField(is_primary_key=True)
    delivery_method = field.CharDBField(max_length=20)
    provider = field.CharDBField(max_length=20)

    location_id = None  # TODO foriengn key

    def serialize(self):
        fields = [
            "ID",
            "delivery_method",
            "provider",
        ]

        return {f: getattr(self, f) for f in fields}


class LocationModel(model.BaseDBModel):
    __tablename__ = "location"

    ID = field.IntegerDBField(is_primary_key=True)
    name = field.CharDBField(max_length=20)
    is_main_city = field.BooleanDBField()
    delivery_cost = field.FloatDBField()

    def serialize(self):
        fields = [
            "ID",
            "name",
            "is_main_city",
            "delivery_cost",
        ]

        return {f: getattr(self, f) for f in fields}

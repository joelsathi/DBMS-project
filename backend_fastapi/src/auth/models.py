from ..core import model, field


class PaymentDetailDBModel(model.BaseDBModel):
    __tablename__ = "payment_detail"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    card_no = field.CharDBField(max_length=20)
    provider = field.CharDBField(max_length=20)

    def serialize(self):
        fields = [
            "id",
            "card_no",
            "provider",
        ]

        return {f: getattr(self, f) for f in fields}


class RegisteredUserDBModel(model.BaseDBModel):
    __tablename__ = "registered_user"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    username = field.CharDBField(max_length=255)
    password = field.CharDBField(max_length=512)
    firstname = field.CharDBField(max_length=255)
    lastname = field.CharDBField(max_length=255)
    email = field.CharDBField(max_length=255)
    address = field.CharDBField(max_length=512, allow_null=True)
    mobile_no = field.CharDBField(max_length=10)
    is_admin = field.BooleanDBField()
    created_date = None  # TODO
    payment_detail_id = field.ForeignKeyDBField(
        related_model=PaymentDetailDBModel, allow_null=True
    )

    def serialize(self):
        fields = [
            "id",
            "username",
            "firstname",
            "lastname",
            "email",
            "address",
            "mobile_no",
            "payment_detail_id",
            "is_admin",
        ]

        return {f: getattr(self, f) for f in fields}


class UserDBModel(model.BaseDBModel):
    __tablename__ = "user"

    id = field.IntegerDBField(is_primary_key=True, auto_generated=True)
    is_guest = field.BooleanDBField()
    registered_user_id = field.ForeignKeyDBField(related_model=RegisteredUserDBModel)

    def serialize(self):
        fields = ["id", "is_guest", "registered_user_id"]

        return {f: getattr(self, f) for f in fields}

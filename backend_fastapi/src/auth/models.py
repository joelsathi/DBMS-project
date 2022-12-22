from ..core import model, field


class RegisteredUserDBModel(model.BaseDBModel):
    __tablename__ = "registered_user"

    id = field.IntegerDBField(is_primary_key=True)
    username = field.CharDBField(max_length=255)
    password = field.CharDBField(max_length=512)
    firstname = field.CharDBField(max_length=255)
    lastname = field.CharDBField(max_length=255)
    email = field.CharDBField(max_length=255)
    address = field.CharDBField(max_length=512, allow_null=True)
    mobile_no = field.CharDBField(max_length=10)
    created_date = None  # TODO
    payment_detail_id = None  # TODO

    def serialize(self):
        fields = [
            "id",
            "username",
            "firstname",
            "lastname",
            "email",
            "address",
            "mobile_no",
        ]

        return {f: getattr(self, f) for f in fields}


class UserDBModel(model.BaseDBModel):
    __tablename__ = "user"

    # TODO complete

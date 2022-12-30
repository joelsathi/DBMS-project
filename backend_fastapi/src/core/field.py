from functools import cached_property


DEFAULT_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"


class InvalidRelatedModelException(Exception):
    pass


class BaseDBField:
    def __init__(self, allow_null=False, default=None, is_primary_key=False):
        self.allow_null = allow_null
        self.is_primary_key = is_primary_key
        self.default = default

        self.name = None

    def set_name(self, name):
        self.name = name

    def from_db(self, value):
        """Convert value obtained from database (from the connector) into the relevant python type"""
        return value

    def to_db(self, value):
        """Convert python type to format that can be saved in database"""
        return value

    def get_default(self):
        if callable(self.default):
            return self.default()
        return self.default


class IntegerDBField(BaseDBField):
    def from_db(self, value):
        if isinstance(value, int) or value is None:
            return value
        return int(value)


class CharDBField(BaseDBField):
    def __init__(self, *args, max_length=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    def from_db(self, value):
        if isinstance(value, str) or value is None:
            return value
        return str(value)

    def to_db(self, value):
        return str(value)


class TextDBField(BaseDBField):
    def from_db(self, value):
        if isinstance(value, str) or value is None:
            return value
        return str(value)

    def to_db(self, value):
        return str(value)


class DateTimeDBField(BaseDBField):
    def __init__(self, *args, datetime_format=DEFAULT_DATETIME_FORMAT, **kwargs):
        super().__init__(*args, **kwargs)
        self.datetime_format = datetime_format

    def from_db(self, value):
        raise NotImplementedError

    def to_db(self, value):
        raise NotImplementedError


class FloatDBField(BaseDBField):
    def from_db(self, value):
        if isinstance(value, float) or value is None:
            return value
        return round(float(value), 2)

    def to_db(self, value):
        raise NotImplementedError


class BooleanDBField(BaseDBField):
    def from_db(self, value):
        if isinstance(value, bool) or value is None:
            return value
        return bool(value)

    def to_db(self, value):
        return bool(value)


class ForeignKeyDBField(BaseDBField):
    def __init__(self, *args, related_model, **kwargs):
        super().__init__(*args, **kwargs)
        self.related_model = related_model
        self._check_valid_relation()

    def set_name(self, name):
        _name = name
        if _name.split("_")[-1] == "id":
            _name = _name[:-3]
        super().set_name(_name)

    @cached_property
    def name_id(self):
        return self.name + "_id"

    def _check_valid_relation(self):
        if getattr(self.related_model, "__tablename__", None) is None:
            raise InvalidRelatedModelException(
                "{} is not a valid related model!".format(self.related_model)
            )

    def from_db(self, value):
        if isinstance(value, int) or value is None:
            return value
        return int(value)

    def to_db(self, value):
        raise NotImplementedError

from functools import cached_property
import datetime

DEFAULT_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"


class FieldException(Exception):
    pass


class ValidationException(Exception):
    pass


class LazyFieldAttribute:
    """
    To set related objects as attributes on model instances without immediately running a query
    when instantiating the instance. This would be useful to get a list of model instances from a
    single query without having to run a query for each related object when instantiating each
    instance from the query results, while at the same time having an easy way to query and access
    the related object when dealing with individual model instances.
    """

    def __init__(self, field, getter, pre_setter):
        self.field = field
        self.getter = getter
        self.pre_setter = pre_setter

    def __get__(self, instance, cls=None):
        if instance is None:
            return self.field

        if self.field.name in instance.__dict__:
            return instance.__dict__[self.field.name]

        field_value = self.getter(instance)
        instance.__dict__[self.field.name] = field_value
        return field_value

    def __set__(self, instance, value):
        # TODO do we do some basic type checking here?
        self.pre_setter(instance, value)
        instance.__dict__[self.field.name] = value


class BaseDBField:
    def __init__(
        self,
        allow_null=False,
        default=None,
        is_primary_key=False,
        validators=[],
        auto_generated=False,
    ):
        self.allow_null = allow_null
        self.is_primary_key = is_primary_key
        self.default = default
        self.auto_generated = auto_generated

        for validator in validators:
            if not callable(validator):
                raise FieldException(
                    "Invalid validator {}. All validators must be callables".format(
                        validator
                    )
                )
        self.validators = validators

        self.name = None

    def _validate(self, value):
        if not self.allow_null and value is None and not self.auto_generated:
            raise ValidationException("Field {} cannot be null".format(self.name))

    def validate(self, value):
        """
        Will throw an exception if data is invalid for field. This method is expected to be called
        before saving or updating an instance to make sure that the
        """

        self._validate(value)
        for validator in self.validators:
            validator(value)

    def add_to_model(self, model_name, field_name, new_attrs):
        """Add this field to a model

        NOTE: This will be called inside a metaclasses __new__ method, so we will directly be
        working with attribute dictionaries.

        Args:
            model_name (str): name of the model class we're working with
            field_name (str): name of field on the model class
            new_attrs (dict): dict which will have all the attributes to be added to the model
                classes __dict__. This would have a dict _field inside it containing fields of the
                model.
        """

        self.name = field_name
        new_attrs["_fields"][self.name] = self

        if self.is_primary_key:
            # NOTE: for now, we will not allow multiple primary keys
            if "primary_key" in new_attrs:
                raise FieldException(
                    "Cannot add multiple primary keys '{}' and '{}' to model {}".format(
                        self.name, new_attrs["primary_key"], model_name
                    )
                )
            new_attrs["primary_key"] = self.name

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
        # return datetime.datetime.strptime(value, self.datetime_format)
        # It appears the connector internally converts datetime fields to python datetime objects
        return value

    def to_db(self, value):
        return value.strftime(self.datetime_format)


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
    # TODO consider reverse side of relationship too

    def __init__(self, *args, related_model, **kwargs):
        super().__init__(*args, **kwargs)
        self.related_model = related_model
        self._check_valid_relation()

    @cached_property
    def name_id(self):
        return self.name + "_id"

    def _check_valid_relation(self):
        if getattr(self.related_model, "__tablename__", None) is None:
            raise FieldException(
                "{} is not a valid related model!".format(self.related_model)
            )

    def from_db(self, value):
        if isinstance(value, int) or value is None:
            return value
        return int(value)

    def to_db(self, value):
        raise NotImplementedError

    def get_related_object(self, instance):
        related_obj_id = getattr(instance, self.name_id)
        if related_obj_id is None:
            return None
        return self.related_model.objects.select_by_id(related_obj_id)

    def set_related_object_id(self, instance, obj):
        setattr(instance, self.name_id, getattr(obj, obj.primary_key))

    def add_to_model(self, model_name, field_name, new_attrs):
        """Add this field to a model

        NOTE: This will be called inside a metaclasses __new__ method, so we will directly be
        working with attribute dictionaries.

        Args:
            model_name (str): name of the model class we're working with
            field_name (str): name of field on the model class
            new_attrs (dict): dict which will have all the attributes to be added to the model
                classes __dict__. This would have a dict _field inside it containing fields of the
                model.
        """

        _name = field_name
        if _name.split("_")[-1] == "id":
            _name = _name[:-3]
        self.name = _name

        new_attrs["_foreign_key_fields"][self.name] = self
        new_attrs[self.name] = LazyFieldAttribute(
            self, self.get_related_object, self.set_related_object_id
        )

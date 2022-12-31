from functools import lru_cache
from .manager import BaseQueryManager
from .field import BaseDBField, ForeignKeyDBField


class MetaModel(type):
    __query_manager__ = BaseQueryManager

    def __new__(cls, name, bases, attrs, **kwargs):
        # return if we're dealing with the BaseDBModel class (We only want to deal with concrete
        # classes here)
        top_level = True
        for base in bases:
            if isinstance(base, MetaModel):
                top_level = False
                break
        if top_level:
            return super().__new__(cls, name, bases, attrs)

        # initialize fields with names and define as an attribute on the class
        new_attrs = {}
        new_attrs["_fields"] = {}
        new_attrs["_foreign_key_fields"] = {}
        for attr_name, attr in attrs.items():
            if isinstance(attr, BaseDBField):
                attr.add_to_model(
                    model_name=name,
                    field_name=attr_name,
                    new_attrs=new_attrs,
                )
            else:
                new_attrs[attr_name] = attr

        return super().__new__(cls, name, bases, new_attrs)

    @property
    def objects(cls):
        """Syntactic sugar to obtain a manager instance for the class"""
        return cls.__query_manager__(model_class=cls)

    @lru_cache(maxsize=1)
    def get_field_names(cls):
        return {
            **cls._fields,
            **{f.name_id: f for f in cls._foreign_key_fields.values()},
        }

    @lru_cache(maxsize=1)
    def get_fields(self):
        return [*self._fields.values(), *self._foreign_key_fields.values()]


class BaseDBModel(metaclass=MetaModel):
    """Base Model class from which to inherit db models.

    NOTE: Only final model classes should inherit from this.
    """

    __tablename__ = None

    def __init__(self, *args, **kwargs):
        """NOTE: For now make sure that all field values are passed as kwargs"""

        for f in self._fields.values():
            try:
                value = kwargs[f.name]
            except KeyError:
                value = f.get_default()
            setattr(self, f.name, value)

        for f in self._foreign_key_fields.values():
            try:
                value = kwargs[f.name]  # entire related object
                setattr(self, f.name, value)
            except KeyError:
                try:
                    value = kwargs[f.name_id]  # id only
                except KeyError:
                    value = None
                setattr(self, f.name_id, value)

        # TODO check for extra kwargs / args

    def save(self):
        raise NotImplementedError

    def serialize(self):
        """Convert the model object into a representation suitable for sending as an API response.

        NOTE: This would generally need to be overridden by every model class since the fields needed
        to be sent per response would vary depending on each models needs.

        Returns:
            Generally a dict with the relevant model fields and values would be returned.
        """

        return {f: getattr(self, f) for f in self.get_field_names()}

    def serialize_with_related(self):
        """
        Convert the model object into a representation suitable for sending as an API response,
        including a representation of related objects. Similar to `serialize`, except this would
        include nested related objects instead of just their ids.
        """

        serialized_obj = {}

        for f in self.__class__.get_fields():
            if isinstance(f, ForeignKeyDBField):
                serialized_obj[f.name] = f.related_model.serialize(
                    getattr(self, f.name)
                )

            else:
                serialized_obj[f.name] = getattr(self, f.name)

        return serialized_obj

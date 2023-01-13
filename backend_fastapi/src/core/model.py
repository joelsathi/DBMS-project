from functools import lru_cache
from .manager import BaseQueryManager
from .field import BaseDBField, ForeignKeyDBField


class DBModelException(Exception):
    pass


class ModelInstanceException(Exception):
    pass


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

        if "primary_key" not in new_attrs:
            raise DBModelException("Model {} does not have a primary key!".format(name))

        return super().__new__(cls, name, bases, new_attrs)

    @property
    def objects(cls):
        """Syntactic sugar to obtain a manager instance for the class"""
        return cls.__query_manager__(model_class=cls)

    @lru_cache(maxsize=1)
    def get_fields_by_name(cls):
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

    def __init__(self, *args, is_existing=False, **kwargs):
        """NOTE: For now make sure that all field values are passed as kwargs"""

        self.is_existing = is_existing

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
        # Insert if record doesn't exist in db
        if not self.is_existing:
            field_dict = {}
            for fname, field in self._fields.items():
                fval = getattr(self, fname)
                # perform validation on field values
                field.validate(fval)
                field_dict[fname] = fval
            for fname, field in self._foreign_key_fields.items():
                fval = getattr(self, field.name_id)
                # perform validation on field values
                field.validate(fval)
                field_dict[field.name_id] = fval

            insert_success, row_id = self.__class__.objects._insert(
                field_dict=field_dict
            )
            if (
                insert_success
                and getattr(self, self.primary_key) is None
                and self._fields[self.primary_key].auto_generated
            ):
                # update pk if relevant and insert is successful
                setattr(self, self.primary_key, row_id)

            return insert_success

        # Otherwise update existing record
        else:
            field_dict = {}
            for fname, field in self._fields.items():
                fval = getattr(self, fname)
                if fname == self.primary_key:
                    pk_val = getattr(self, self.primary_key)
                    if pk_val is None:
                        raise ModelInstanceException(
                            "Can't save {} instance without specifying pk {}".format(
                                self.__class__.__qualname__, self.primary_key
                            )
                        )

                elif fval is not None:
                    # perform validation on field values
                    field.validate(fval)
                    field_dict[fname] = fval

            for fname, field in self._foreign_key_fields.items():
                fval = getattr(self, fname)
                if fval is not None:
                    # perform validation on field values
                    field.validate(fval)
                    field_dict[field.name_id] = fval

            update_success = self.__class__.objects._update(
                field_dict=field_dict, filter_dict={self.primary_key: pk_val}
            )

            return update_success

        # TODO
        # validate -> call validate method on each field, any model specific validation?
        # save -> manager save method, manager update method
        # how to know if updating or saving?
        # save related here too?

    def remove(self):
        # nothing to remove if its not already marked as being in the database
        if self.is_existing:
            pk_val = getattr(self, self.primary_key)
            delete_success = self.__class__.objects._delete(
                filter_dict={self.primary_key: pk_val}
            )
            return delete_success

    def __repr__(self) -> str:
        return "<{} object {}>".format(
            self.__class__.__qualname__, getattr(self, self.primary_key)
        )

    def serialize(self):
        """Convert the model object into a representation suitable for sending as an API response.

        NOTE: This would generally need to be overridden by every model class since the fields needed
        to be sent per response would vary depending on each models needs.

        Returns:
            Generally a dict with the relevant model fields and values would be returned.
        """

        return {f: getattr(self, f) for f in self.get_fields_by_name()}

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

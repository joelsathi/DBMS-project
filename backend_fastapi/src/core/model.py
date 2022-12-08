from .manager import BaseManager


class MetaManagedModel(type):
    __managerclass__ = BaseManager

    @property
    def manager(cls):
        return cls.__managerclass__(model_class=cls)


class BaseDBModel(metaclass=MetaManagedModel):
    __tablename__ = None

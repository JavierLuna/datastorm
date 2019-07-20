import inspect
from typing import Optional, Union

from google.cloud import datastore
from google.cloud.datastore import Entity, Key

from datastorm.fields import BaseField, AnyField
from datastorm.query import QueryBuilder


class AbstractDSEntity(type):

    @property
    def query(cls):
        return QueryBuilder(cls)

    def __getattribute__(self, key):
        attr = super(AbstractDSEntity, self).__getattribute__(key)
        if isinstance(attr, BaseField) and attr.field_name is None:
            attr.field_name = key
        return attr


class BaseEntity:
    __kind__ = None
    __base_filters__ = []
    _datastore_client = None

    def __init__(self, key: Union[Key, str], _kind: Optional[str] = None, _project: Optional[str] = None,
                 _raw_entity: Optional[Entity] = None, **kwargs):
        self.key = key if type(key) is not str else self.generate_key(key)
        self.__raw_entity = _raw_entity
        self.__datastorm_fields = {attr_name: attr for attr_name, attr in
                                   [(field_name, getattr(self, field_name)) for field_name in dir(self)] if
                                   isinstance(attr, BaseField)}
        [self.set(name, field.default) for name, field in self.__datastorm_fields.items()]
        [self.set(name, value) for name, value in kwargs.items()]
        self._save_offline()

    def save(self, force_sync=False):
        self._save_offline()
        if force_sync:
            self.sync()
        self._datastore_client.put(self.__raw_entity)

    def set(self, name, value, field=AnyField):
        field = self.__datastorm_fields.get(value, field)
        self.__datastorm_fields[name] = field if field in self.__datastorm_fields or \
                                                 not inspect.isclass(field) else field()
        setattr(self, name, value)

    def sync(self):
        buffer = self.__raw_entity
        self.__raw_entity = self._datastore_client.get(self.key)
        self.__raw_entity.update(buffer)

    def _save_offline(self, exclude_from_indexes: tuple = ()):
        self.__raw_entity = self.__raw_entity or datastore.Entity(key=self.key,
                                                                  exclude_from_indexes=exclude_from_indexes)
        entity_dict = {attr_name: field.dumps(getattr(self, attr_name)) for attr_name, field in
                       self.__datastorm_fields.items()}
        self.__raw_entity.update(entity_dict)

    def delete(self):
        """Delete the object from Datastore."""
        self._datastore_client.delete(self.key)

    @classmethod
    def generate_key(cls, identifier: str, parent_key: Optional[Key] = None):
        return cls._datastore_client.key(cls.__kind__, identifier, parent=parent_key)

    def get_raw_entity(self):
        return self.__raw_entity

    def __repr__(self):
        return "< {name} >".format(name=self.__kind__)  # pragma: no cover

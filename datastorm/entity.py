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

    def __init__(self, key: Union[Key, str], _raw_entity: Optional[Entity] = None, **kwargs):
        self.key = key if type(key) is not str else self.generate_key(key)
        self.__datastorm_fields = self.__resolve_mappings()

        [self.set(name, field.default) for name, field in self.__datastorm_fields.items()]
        [self.set(name, value) for name, value in kwargs.items()]

    def save(self):
        self._datastore_client.put(self.get_datastore_entity())

    def set(self, name, value, field=None):
        field = field or self.__datastorm_fields.get(value, AnyField)
        self.__datastorm_fields[name] = field if field in self.__datastorm_fields or \
                                                 not inspect.isclass(field) else field()
        setattr(self, name, value)

    def sync(self):
        buffer = self.get_datastore_entity()
        updated_instance = self._datastore_client.get(self.key)
        for field_name, datastore_value in updated_instance.items():
            if field_name not in buffer or buffer[field_name] != updated_instance[field_name]:
                self.set(field_name, datastore_value)
    def delete(self):
        """Delete the object from Datastore."""
        self._datastore_client.delete(self.key)

    @classmethod
    def generate_key(cls, identifier: str, parent_key: Optional[Key] = None):
        return cls._datastore_client.key(cls.__kind__, identifier, parent=parent_key)

    def get_datastore_entity(self):
        entity = datastore.Entity(key=self.key)
        entity_dict = {field_name: field.dumps(getattr(self, field_name)) for field_name, field in
                       self.__datastorm_fields.items()}
        entity.update(entity_dict)
        return entity

    def __resolve_mappings(self):
        field_mapping = {}
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if inspect.isclass(attribute) and issubclass(attribute, BaseField):
                attribute = attribute()
            if isinstance(attribute, BaseField):
                field_mapping[attribute_name] = attribute
        return field_mapping

    def __repr__(self):
        return "< {name} >".format(name=self.__kind__)  # pragma: no cover

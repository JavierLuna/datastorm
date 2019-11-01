import inspect
from typing import Optional, Union, Any, List, Type

from google.cloud import datastore
from google.cloud.datastore import Key

from datastorm.fields import BaseField
from datastorm.filter import Filter
from datastorm.mapper import FieldMapper
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
    __kind__: str = None  # type: ignore
    __base_filters__: List[Filter] = []

    _datastore_client = None

    def __init__(self, key: Union[Key, str], **kwargs):
        self.key = key if type(key) is not str else self.generate_key(key)
        self._datastorm_mapper = self.__resolve_mappings()
        self.__set_defaults()

        [self.set(name, value) for name, value in kwargs.items()]

    def save(self):
        self._datastore_client.put(self.get_datastore_entity())

    def set(self, field_name: str, value: Any, field: Optional[BaseField] = None):
        if field:
            self._map_field(field_name, field)
        if field_name not in self._datastorm_mapper.fields:
            self._datastorm_mapper.set_field(field_name, self._datastorm_mapper.get_field(field_name))

        setattr(self, field_name, value)

    def _map_field(self, field_name: str, field: Union[BaseField, Type[BaseField]]):
        field_instance = field() if inspect.isclass(field) else field  # type: ignore
        self._datastorm_mapper.set_field(field_name, field_instance)  # type: ignore

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
        return cls._datastore_client.key(cls.__kind__, identifier, parent=parent_key)  # type: ignore

    def get_datastore_entity(self):
        entity = datastore.Entity(key=self.key)
        for field_name in self._datastorm_mapper.fields:
            field = self._datastorm_mapper.get_field(field_name)

            entity_dict = {field.field_name or field_name: field.dumps(getattr(self, field_name))}
            entity.update(entity_dict)
        return entity

    def __resolve_mappings(self) -> FieldMapper:
        field_mapper = FieldMapper()
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if inspect.isclass(attribute) and issubclass(attribute, BaseField):
                attribute = attribute()
            if isinstance(attribute, BaseField):
                field_mapper.set_field(attribute_name, attribute)
        return field_mapper

    def __set_defaults(self):
        for field_name in self._datastorm_mapper.fields:
            self.set(field_name, self._datastorm_mapper.default(field_name))

    def __repr__(self):
        return "< {name} >".format(name=self.__kind__)  # pragma: no cover

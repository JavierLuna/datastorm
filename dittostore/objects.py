import datetime
from typing import Union, Optional

from google.cloud import datastore
from google.cloud.datastore import Key, Entity


class FilterField:

    def __init__(self, field_name: str):
        self.field_name = field_name

    def __eq__(self, other: Union[str, int, float, bool]):
        return Query(self.field_name, "=", other)

    def __lt__(self, other: Union[str, int, float, bool]):
        return Query(self.field_name, "<", other)

    def __gt__(self, other: Union[str, int, float, bool]):
        return Query(self.field_name, ">", other)

    def __le__(self, other: Union[str, int, float, bool]):
        return Query(self.field_name, "<=", other)

    def __ge__(self, other: Union[str, int, float, bool]):
        return Query(self.field_name, ">=", other)

    def __repr__(self):
        return self.field_name


class Query:

    def __init__(self, item: str, op: str, value: Union[str, int, float, bool]):
        self.item = item
        self.op = op
        self.value = value

    def __repr__(self):
        return "< Query object: {} {} {} >".format(self.item, self.op, self.value)


class QueryBuilder:

    def __init__(self, entity_class):
        self.__entity_class = entity_class
        self.__project = entity_class.__project__
        self.__kind = entity_class.__kind__
        self.__filters = []
        self.__order = []

    def filter(self, filter: Query):
        self.__filters.append(filter)
        return self

    def order(self, field: Union[FilterField, str], inverted: bool = False):
        field = field.field_name if type(field) is FilterField else field
        field = "-" + field if inverted else field
        self.__order.append(field)
        return self

    def get(self, identifier: Union[Key, str] = None, key: Key = None):
        client = datastore.Client(project=self.__project)
        key = key or client.key(self.__kind, identifier)
        raw_entity = client.get(key)
        return self.__entity_class(key, _raw_entity=raw_entity, **raw_entity)

    def all(self, page_size: int = 500, parent_key: Union[Key, str] = None):
        client = datastore.Client(project=self.__project)

        if parent_key is not None and type(parent_key) is str:
            parent_key = client.key(self.__kind, parent_key)

        query = client.query(kind=self.__kind, ancestor=parent_key)
        [query.add_filter(filter.item, filter.op, filter.value) for filter in self.__filters]

        if self.__order:
            query.order = self.__order

        cursor = None
        while True:
            query_iter = query.fetch(start_cursor=cursor, limit=page_size)
            page = list(next(query_iter.pages))
            for raw_entity in page:
                yield self.__entity_class(raw_entity.key, _raw_entity=raw_entity, **raw_entity)
            cursor = query_iter.next_page_token
            if not page:
                break

    def first(self):
        result = list(self.all(page_size=1))
        return result.pop() if result else None

    def __repr__(self):
        return "< QueryBuilder filters: {}, ordered by: {}>".format(self.__filters or "No filters",
                                                                    self.__order or "No order")


class AbstractDSEntity(type):

    @property
    def query(cls):
        return QueryBuilder(cls)

    def __getattr__(cls, key: str):
        return FilterField(key)


class BaseEntity:
    __kind__ = None
    __project__ = None
    __exclude__ = []
    __allowed_types__ = [str, int, float, bool, datetime.datetime]

    def __init__(self, key: Union[Key, str], _kind: Optional[str] = None, _project: Optional[str] = None,
                 _raw_entity: Optional[Entity] = None, **kwargs):
        self.key = key if type(key) is not str else self.generate_key(key)
        self.__kind__ = _kind or self.__kind__
        self.__project__ = _project or self.__project__
        self.__raw_entity = _raw_entity
        self.__default_excludes = {attr for attr in dir(BaseEntity)}
        [setattr(self, name, value) for name, value in kwargs.items()]
        self._save_offline()

    def save(self, exclude_from_indexes: tuple = ()):
        client = datastore.Client(project=self.__project__)
        self._save_offline(exclude_from_indexes)

        client.put(self.__raw_entity)

    def _save_offline(self, exclude_from_indexes: tuple = ()):
        self.__raw_entity = self.__raw_entity or datastore.Entity(key=self.key,
                                                                  exclude_from_indexes=exclude_from_indexes)
        fields_to_store = {attr for attr in dir(self) if
                           type(getattr(self, attr)) in self.__allowed_types__} - self.__default_excludes
        entity_dict = {attr: getattr(self, attr) for attr in fields_to_store}
        self.__raw_entity.update(entity_dict)

    def delete(self):
        """Delete the object from Datastore."""
        client = datastore.Client(project=self.__project__)
        client.delete(self.__raw_entity.key)

    @classmethod
    def generate_key(cls, identifier: str, parent_key: Optional[Key] = None):
        return datastore.Client(project=cls.__project__).key(cls.__kind__, identifier, parent=parent_key)

    def get_raw_entity(self):
        return self.__raw_entity

    def __repr__(self):
        return "< {name} >".format(name=self.__kind__)

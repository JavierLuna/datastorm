import datetime
import json
from typing import Union, Optional, List

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
        return self.field_name  # pragma: no cover


class Query:

    def __init__(self, item: str, op: str, value: Union[str, int, float, bool]):
        self.item = item
        self.op = op
        self.value = value

    def __repr__(self):
        return "< Query object: {} {} {} >".format(self.item, self.op, self.value)  # pragma: no cover


class QueryBuilder:

    def __init__(self, entity_class):
        self.__entity_class = entity_class
        self.__project = entity_class.__project__
        self.__kind = entity_class.__kind__
        self.__client = entity_class.__datastorm_client__
        self.__filters = entity_class.__base_filters__ or []
        self.__projection = []
        self.__order = []

    def filter(self, *filters: Query):
        self.__filters += filters
        return self

    def order(self, field: Union[FilterField, str], inverted: bool = False):
        field = field.field_name if type(field) is FilterField else field
        field = "-" + field if inverted else field
        self.__order.append(field)
        return self

    def only(self, *args: List[str]):
        self.__projection += args
        return self

    def get(self, identifier: Union[Key, str] = None, key: Key = None):
        key = key or self.__client.key(self.__kind, identifier)
        raw_entity = self.__client.get(key)

        return None if raw_entity is None else self.__entity_class(key, _raw_entity=raw_entity, **raw_entity)

    def all(self, page_size: int = 500, parent_key: Key = None):

        query = self.__client.query(kind=self.__kind, ancestor=parent_key)
        [query.add_filter(filter.item, filter.op, filter.value) for filter in self.__filters]

        if self.__order:
            query.order = self.__order

        if self.__projection:
            query.projection = self.__projection

        cursor = None
        while True:
            last_yielded_entity = None
            query_iter = query.fetch(start_cursor=cursor, limit=page_size)
            for raw_entity in query_iter:
                last_yielded_entity = self.__entity_class(raw_entity.key, _raw_entity=raw_entity, **raw_entity)
                yield last_yielded_entity
            cursor = query_iter.next_page_token
            if not cursor or last_yielded_entity is None:
                break

    def first(self):
        result = None
        try:
            result = next(self.all(page_size=1))
        except TypeError:  # pragma: no cover
            pass
        except StopIteration:  # pragma: no cover
            pass

        return result

    def __repr__(self):
        return "< QueryBuilder filters: {}, ordered by: {}>".format(self.__filters or "No filters",
                                                                    self.__order or "No order")  # pragma: no cover


class AbstractDSEntity(type):

    @property
    def query(cls):
        return QueryBuilder(cls)

    def __getattr__(cls, key: str):
        return FilterField(key)


class BaseEntity:
    __kind__ = None
    __project__ = None
    __base_filters__ = []
    __exclude__ = []
    __datastorm_client__ = None
    __allowed_types__ = [str, int, float, bool, datetime.datetime, dict, list]

    def __init__(self, key: Union[Key, str], _kind: Optional[str] = None, _project: Optional[str] = None,
                 _raw_entity: Optional[Entity] = None, **kwargs):
        self.key = key if type(key) is not str else self.generate_key(key)
        self.__kind__ = _kind or self.__kind__
        self.__project__ = _project or self.__project__
        self.__raw_entity = _raw_entity
        self.__default_excludes = {attr for attr in dir(BaseEntity)}
        [setattr(self, name, self._autouncast(name, value)) for name, value in kwargs.items()]
        self._save_offline()

    def save(self, force_sync=False):
        self._save_offline()
        if force_sync:
            self.sync()
        self.__datastorm_client__.put(self.__raw_entity)

    def sync(self):
        buffer = self.__raw_entity
        self.__raw_entity = self.__datastorm_client__.get(self.key)
        self.__raw_entity.update(buffer)

    def _save_offline(self, exclude_from_indexes: tuple = ()):
        self.__raw_entity = self.__raw_entity or datastore.Entity(key=self.key,
                                                                  exclude_from_indexes=exclude_from_indexes)
        fields_to_store = {attr for attr in dir(self) if
                           type(getattr(self, attr)) in self.__allowed_types__ and not attr.startswith(
                               "_")} - self.__default_excludes
        entity_dict = {attr: self._autocast(getattr(self, attr)) for attr in fields_to_store}
        self.__raw_entity.update(entity_dict)

    def _autocast(self, value):
        if type(value) in [list, dict]:
            try:
                return json.dumps(value, sort_keys=True)
            except:  # pragma: no cover
                pass
        return value

    def _autouncast(self, property, value):
        if hasattr(self, property) and type(getattr(self, property)) in [dict, list]:
            try:
                return json.loads(value)
            except:  # pragma: no cover
                pass
        return value

    def delete(self):
        """Delete the object from Datastore."""
        self.__datastorm_client__.delete(self.key)

    @classmethod
    def generate_key(cls, identifier: str, parent_key: Optional[Key] = None):
        return cls.__datastorm_client__.key(cls.__kind__, identifier, parent=parent_key)

    def get_raw_entity(self):
        return self.__raw_entity

    def __repr__(self):
        return "< {name} >".format(name=self.__kind__)  # pragma: no cover

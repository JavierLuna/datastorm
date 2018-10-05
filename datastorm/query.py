from typing import Union, List

from google.cloud.datastore import Key

from datastorm.fields import BaseField
from datastorm.filter import Filter


class QueryBuilder:

    def __init__(self, entity_class):
        self.__entity_class = entity_class
        self.__project = entity_class.__project__
        self.__kind = entity_class.__kind__
        self.__client = entity_class.__datastorm_client__
        self.__filters = entity_class.__base_filters__ or []
        self.__projection = []
        self.__order = []

    def filter(self, *filters: Filter):
        self.__filters += filters
        return self

    def order(self, field: Union[BaseField, str], inverted: bool = False):
        field = field.field_name if isinstance(field, BaseField) else field
        field = "-" + field if inverted else field
        self.__order.append(field)
        return self

    def only(self, *args: List[str]):
        self.__projection += args
        return self

    def get(self, key: Union[Key, str]):
        if not isinstance(key, Key):
            key = self.__client.key(self.__kind, key)
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



from typing import Union, List

from google.cloud import datastore
from google.cloud.datastore import Key

from datastorm.fields import BaseField
from datastorm.filter import Filter


class QueryBuilder:

    def __init__(self, entity_class, filters=None, order=None):
        self._entity_class = entity_class
        self._kind = entity_class.__kind__
        self._client = entity_class._datastore_client
        filters = filters or []
        self._filters = filters + entity_class.__base_filters__
        self._order = order or []

    def filter(self, *filters: Filter):
        self._filters += filters
        return self

    def order(self, field: Union[BaseField, str], inverted: bool = False):
        order_field = field.field_name if isinstance(field, BaseField) else field
        order_field = "-" + order_field if inverted else order_field  # type: ignore
        self._order.append(order_field)
        return self

    def only(self, *args: List[str]):
        return ProjectedQueryBuilder(self._entity_class, filters=self._filters, order=self._order, projection=args)

    def get(self, key: Union[Key, str]):
        if not isinstance(key, Key):
            key = self._client.key(self._kind, key)
        raw_entity = self._client.get(key)

        return None if raw_entity is None else self._make_entity_instance(raw_entity.key, raw_entity)

    def all(self, page_size: int = 500, parent_key: Key = None):

        query = self._get_query(parent_key)
        query = self._build_query(query)

        cursor = None
        while True:
            last_yielded_entity = None
            query_iter = query.fetch(start_cursor=cursor, limit=page_size)
            for raw_entity in query_iter:
                last_yielded_entity = self._make_entity_instance(raw_entity.key, raw_entity)
                yield last_yielded_entity
            cursor = query_iter.next_page_token
            if not cursor or last_yielded_entity is None:
                break

    def _modify_filters(self, query):
        [query.add_filter(filter.item, filter.op, filter.value) for filter in self._filters]
        return query

    def _modify_order(self, query):
        if self._order:
            query.order = self._order
        return query

    def _get_query(self, parent_key: Key):
        query = self._client.query(kind=self._kind, ancestor=parent_key)
        return query

    def _build_query(self, query):
        query = self._modify_filters(query)
        query = self._modify_order(query)
        return query

    def first(self):
        result = None
        try:
            result = next(self.all(page_size=1))
        except TypeError:  # pragma: no cover
            pass
        except StopIteration:  # pragma: no cover
            pass

        return result

    def _make_entity_instance(self, key: Key, attr_data: dict):
        entity = self._entity_class(key)
        for datastore_field_name, serialized_data in attr_data.items():
            datastorm_field_name = entity._datastorm_mapper.resolve_datastore_alias(datastore_field_name)
            entity.set(datastorm_field_name,
                       entity._datastorm_mapper.get_field(datastorm_field_name).loads(serialized_data))
        return entity

    def __repr__(self):
        return "< QueryBuilder filters: {}, ordered by: {}>".format(self._filters or "No filters",
                                                                    self._order or "No order")  # pragma: no cover


class ProjectedQueryBuilder(QueryBuilder):

    def __init__(self, entity_class, filters=None, order=None, projection=None):
        super(ProjectedQueryBuilder, self).__init__(entity_class, filters=filters, order=order)
        self._projection = projection or []

    def only(self, *args: List[str]):
        self._projection += args
        return self

    def _make_entity_instance(self, key: Key, attr_data: dict):
        entity = datastore.Entity(key=key)
        entity.update(attr_data)
        return entity

    def _modify_projection(self, query):
        if self._projection:
            query.projection = self._projection
        return query

    def _build_query(self, query):
        query = super()._build_query(query)
        query = self._modify_projection(query)
        return query

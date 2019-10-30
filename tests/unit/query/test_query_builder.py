from unittest.mock import Mock

import pytest
from google.cloud.datastore import Key

from datastorm.fields import AnyField
from datastorm.query import QueryBuilder, ProjectedQueryBuilder


@pytest.fixture
def mocked_entity(mocked_datastore):
    mocked_entity = Mock()
    mocked_entity.__kind__ = 'test-kind'
    mocked_entity.__base_filters__ = []
    mocked_entity._datastore_client = mocked_datastore
    return mocked_entity


@pytest.fixture
def qbuilder(mocked_entity):
    return QueryBuilder(mocked_entity)


@pytest.fixture
def mocked_query():
    return Mock()


def test_init_kind_is_entity_kind(qbuilder):
    assert qbuilder._entity_class.__kind__ == qbuilder._kind


def test_init_no_filters_base_filters_add_up(mocked_entity):
    entity_filters = [1, 2, 3]
    mocked_entity.__base_filters__ = entity_filters
    builder = QueryBuilder(mocked_entity, filters=[])
    assert builder._filters == entity_filters


def test_init_filters_base_filters_add_up(mocked_entity):
    base_filters = [4, 2, 3]
    entity_filters = [1, 2, 3]
    mocked_entity.__base_filters__ = entity_filters
    builder = QueryBuilder(mocked_entity, filters=base_filters)
    assert builder._filters == base_filters + entity_filters


def test_filter_adds_filters(qbuilder):
    new_filters = [1, 2, 3]
    qbuilder.filter(*new_filters)
    assert qbuilder._filters == new_filters


def test_filter_empty_no_add(qbuilder):
    qbuilder.filter()
    assert qbuilder._filters == []


@pytest.mark.parametrize("field, inverted, expected", [("test", False, "test"),
                                                       ("test", True, "-test"),
                                                       (AnyField(field_name="test"), False, "test"),
                                                       (AnyField(field_name="test"), True, "-test"),
                                                       ])
def test_order(qbuilder, field, inverted, expected):
    qbuilder.order(field, inverted)
    assert qbuilder._order == [expected]


def test_only_returns_projected_query(qbuilder):
    assert isinstance(qbuilder.only("test"), ProjectedQueryBuilder)


def test_projected_query_has_same_instance(qbuilder):
    assert qbuilder.only("test")._entity_class == qbuilder._entity_class


def test_projected_query_has_same_filters(qbuilder):
    filters = [1, 2, 3]
    qbuilder.filter(*filters)
    assert qbuilder.only("test")._filters == qbuilder._filters


def test_projected_query_has_same_order(qbuilder):
    orders = ["a", AnyField("b")]
    qbuilder.order(orders[0], False)
    qbuilder.order(orders[1], True)
    assert qbuilder.only("test")._order == qbuilder._order


def test_projected_query_has_projected_args(qbuilder):
    projections = (1, 2, 3)
    assert qbuilder.only(*projections)._projection == projections


def test_get_str_generates_key(qbuilder):
    qbuilder.get("test")
    assert qbuilder._client.key.called


def test_get_key_doesnt_generate_key(qbuilder):
    qbuilder.get(Key("test", project="test"))
    assert not qbuilder._client.key.called


@pytest.mark.parametrize("key", ["test", Key("test", project="test")])
def test_get_calls_datastore_get(qbuilder, key):
    qbuilder.get(key)
    assert qbuilder._client.get.called


def test_get_returns_none_if_no_results(qbuilder):
    qbuilder._client.get.return_value = None
    assert qbuilder.get("test") is None


def test_get_returns_datastorm_mapping(qbuilder, mocker):
    mocked_make_entity = mocker.patch('datastorm.query.QueryBuilder._make_entity_instance')
    qbuilder._client.get.return_value = Mock()
    qbuilder.get(Key("test", project="test"))
    assert mocked_make_entity.called


@pytest.mark.parametrize("n_filters", [0, 1, 4])
def test_modify_filters_calls_add_filters_n_filters(n_filters, qbuilder, mocked_datastore, mocked_query):
    qbuilder._filters = [Mock()] * n_filters
    qbuilder._modify_filters(mocked_query)
    assert mocked_query.add_filter.call_count == n_filters


def test_modify_filters_returns_query(qbuilder, mocked_query):
    assert qbuilder._modify_filters(mocked_query) is mocked_query


def test_modify_order_empty_order(qbuilder, mocked_datastore, mocked_query):
    qbuilder._order = []
    mocked_query.order = None
    qbuilder._modify_order(mocked_query)
    assert mocked_query.order is None


def test_modify_order_ok(qbuilder, mocked_datastore, mocked_query):
    orders = [1, 2, 3]
    qbuilder._order = orders
    qbuilder._modify_order(mocked_query)
    assert mocked_query.order == orders


def test_modify_order_returns_query(qbuilder, mocked_query):
    assert qbuilder._modify_order(mocked_query) is mocked_query


def test_get_query_proxies_datastore_client(qbuilder):
    qbuilder._get_query(None)
    assert qbuilder._client.query.called


def test_get_query_passes_kind(qbuilder):
    qbuilder._kind = 123
    qbuilder._get_query(None)
    assert qbuilder._client.query.call_args[1]['kind'] == qbuilder._kind


def test_get_query_passes_parent_key(qbuilder):
    parent_key = 'test-parent-key'
    qbuilder._get_query(parent_key)
    assert qbuilder._client.query.call_args[1]['ancestor'] == parent_key


def test_build_query_calls_modify_orders(qbuilder, mocked_query, mocker):
    mocker.patch('datastorm.query.QueryBuilder._modify_filters')
    mocked_modify_orders = mocker.patch('datastorm.query.QueryBuilder._modify_order')
    qbuilder._build_query(Mock())
    assert mocked_modify_orders.called


def test_build_query_calls_modify_filters(qbuilder, mocked_query, mocker):
    mocked_modify_filters = mocker.patch('datastorm.query.QueryBuilder._modify_filters')
    mocker.patch('datastorm.query.QueryBuilder._modify_order')
    qbuilder._build_query(Mock())
    assert mocked_modify_filters.called


def test_build_query_returns_query(qbuilder, mocked_query):
    assert qbuilder._build_query(mocked_query) is mocked_query

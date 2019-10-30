import pytest

from datastorm.fields import AnyField
from datastorm.mapper import FieldMapper


@pytest.fixture
def mapper():
    return FieldMapper()


@pytest.fixture
def field_name():
    return "test_name"


@pytest.fixture
def field_value():
    return AnyField()


def test_get_field_field_doesnt_exist_returns_anyfield(mapper, field_name):
    assert type(mapper.get_field(field_name)) is AnyField


def test_get_field_same_fieldname(mapper, field_name, field_value):
    mapper._mappings = {field_name: field_value}
    assert mapper.get_field(field_name) == field_value


def test_get_field_different_datastore_name(mapper, field_name, field_value):
    datastore_name = "datastore_test_name"

    mapper._mappings = {field_name: field_value}
    mapper._datastore_mappings = {datastore_name: field_name}
    assert mapper.get_field(datastore_name) == field_value


def test_default_field(mapper, field_name, field_value):
    mapper._mappings = {field_name: field_value}
    assert mapper.default(field_name) == field_value.default

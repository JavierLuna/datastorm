import pytest

from datastorm.fields import ListField


@pytest.fixture
def field():
    return ListField()


def test_check_type_list_ok(field):
    assert field.check_type([])


def test_check_type_no_list_ko(field):
    assert not field.check_type("test")

import pytest

from datastorm.fields import DictField


@pytest.fixture
def field():
    return DictField()


def test_check_type_dict_ok(field):
    assert field.check_type({})


def test_check_type_no_dict_ko(field):
    assert not field.check_type("test")

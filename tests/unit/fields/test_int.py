import pytest

from datastorm.fields import IntField


@pytest.fixture
def field():
    return IntField()


def test_check_type_int_ok(field):
    assert field.check_type(3)


def test_check_type_no_int_ko(field):
    assert not field.check_type("test")


def test_dumps_integers(field):
    assert type(field.dumps(1.03)) is int

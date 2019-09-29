import pytest

from datastorm.fields import FloatField


@pytest.fixture
def field():
    return FloatField()


def test_check_type_float_ok(field):
    assert field.check_type(1.03)


def test_check_type_no_float_ko(field):
    assert not field.check_type("test")


def test_dumps_floats(field):
    assert type(field.dumps(1)) is float

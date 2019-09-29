import pytest

from datastorm.fields import BooleanField


@pytest.fixture
def field():
    return BooleanField()


def test_check_type_boolean_ok(field):
    assert field.check_type(True)


def test_check_type_no_boolean_ko(field):
    assert not field.check_type("test")


def test_dumps_booleans(field):
    assert type(field.dumps(1)) is bool

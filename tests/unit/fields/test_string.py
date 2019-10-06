import pytest

from datastorm.fields import StringField


@pytest.fixture
def field():
    return StringField()


def test_check_type_string_ok(field):
    assert field.check_type("test")


def test_check_type_no_string_ko(field):
    assert not field.check_type(1)


def test_dumps_strings(field):
    assert type(field.dumps(1)) is str

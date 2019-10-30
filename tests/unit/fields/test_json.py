import pytest

from datastorm.fields import JSONField


@pytest.fixture
def field():
    return JSONField()


@pytest.mark.parametrize("value", [bool(), int(), str(), dict(), list()])
def test_check_type_ok(field, value):
    assert field.check_type(value)


def test_check_type_ko(field):
    assert not field.check_type(set())


@pytest.mark.parametrize("value", [bool(), int(), str(), dict(), list()])
def test_dumps_json_str(field, value):
    assert type(field.dumps(value)) == str


@pytest.mark.parametrize("value", [bool(), int(), str(), dict(), list()])
def test_dumps_loads_same_value(field, value):
    assert field.loads(field.dumps(value)) == value


def test_default_is_empty_dict(field):
    assert field.default == {}

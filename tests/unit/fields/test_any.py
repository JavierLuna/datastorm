import operator

import pytest

from datastorm.fields import BaseField, AnyField


@pytest.fixture
def field():
    return AnyField


def test_callable_default(field):
    default_value = "test"
    field = field(default=lambda: default_value)
    assert field.default == default_value


def test_value_default(field):
    default_value = "test"
    field = field(default=default_value)
    assert field.default == default_value


def test_enforce_variable_checks_variable_type(mocker, field):
    mock_check_type = mocker.patch('datastorm.fields.AnyField.check_type', return_value=True)
    field = field(enforce_type=True)
    field.dumps("test")
    assert mock_check_type.called


def test_no_enforce_variable_no_checks_variable_type(mocker, field):
    mock_check_type = mocker.patch('datastorm.fields.AnyField.check_type')
    field = field(enforce_type=False)
    field.dumps("test")
    assert not mock_check_type.called


def test_enforce_variable_incorrect_type_raises_value_error(mocker, field):
    mocker.patch('datastorm.fields.AnyField.check_type', return_value=False)
    field = field(enforce_type=True)
    with pytest.raises(ValueError) as e:
        field.dumps("test")


def test_enforce_variable_incorrect_comparison_raises_value_error(mocker, field):
    mocker.patch('datastorm.fields.AnyField.check_type', return_value=False)
    field = field(enforce_type=True)
    with pytest.raises(ValueError) as e:
        field == "test"


@pytest.mark.parametrize("value", [True, False, 1, 1.0, "test", [], {}, object(), Exception])
def test_check_type_anyfield_true(field, value):
    assert field().check_type(value)


def test_eq_generates_eq_filter(field):
    field = field()
    filter = field == 'test'
    assert filter.op == '='


@pytest.mark.parametrize("op", ['=', '<', '<=', '>', '>='])
def test_lt_generates_lt_filter(field, op):
    field = field()
    ops = {
        '=': operator.eq,
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge
    }
    filter = ops[op](field, "test")
    assert filter.op == op

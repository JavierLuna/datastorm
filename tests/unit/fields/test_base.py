import pytest

from datastorm.fields import BaseField


def test_callable_default():
    default_value = "test"
    field = BaseField(default=lambda: default_value)
    assert field.default == default_value


def test_value_default():
    default_value = "test"
    field = BaseField(default=default_value)
    assert field.default == default_value


def test_enforce_variable_checks_variable_type(mocker):
    mock_check_type = mocker.patch('datastorm.fields.BaseField.check_type', return_value=True)
    field = BaseField(enforce_type=True)
    field.dumps("test")
    assert mock_check_type.called


def test_no_enforce_variable_no_checks_variable_type(mocker):
    mock_check_type = mocker.patch('datastorm.fields.BaseField.check_type')
    field = BaseField(enforce_type=False)
    field.dumps("test")
    assert not mock_check_type.called


def test_enforce_variable_incorrect_type_raises_value_error(mocker):
    mocker.patch('datastorm.fields.BaseField.check_type', return_value=False)
    field = BaseField(enforce_type=True)
    with pytest.raises(ValueError) as e:
        field.dumps("test")


def test_enforce_variable_incorrect_comparison_raises_value_error(mocker):
    mocker.patch('datastorm.fields.BaseField.check_type', return_value=False)
    field = BaseField(enforce_type=True)
    with pytest.raises(ValueError) as e:
        field == "test"

import json
from typing import Union, Any
from datastorm.filter import Filter
from datastorm.base import FieldABC


class BaseField(FieldABC):

    def __init__(self, field_name: str = None, enforce_type=False, default=None):
        self.field_name = field_name
        self.enforce_type = enforce_type
        self._default = default if callable(default) else lambda: default

    def loads(self, serialized_value) -> Any:
        return serialized_value

    def dumps(self, value) -> Any:
        if self.enforce_type and not self.check_type(value):
            raise ValueError("Type mismatch for value {} in field {}".format(value, self.__class__.__name__))
        return self._dumps(value)

    @classmethod
    def _dumps(cls, value) -> Any:
        return value

    def check_type(self, value) -> bool:
        return True

    @property
    def default(self):
        return self._default()

    def __eq__(self, other: Union[str, int, float, bool]):
        return Filter(self.field_name, "=", other)

    def __lt__(self, other: Union[str, int, float, bool]):
        return Filter(self.field_name, "<", other)

    def __gt__(self, other: Union[str, int, float, bool]):
        return Filter(self.field_name, ">", other)

    def __le__(self, other: Union[str, int, float, bool]):
        return Filter(self.field_name, "<=", other)

    def __ge__(self, other: Union[str, int, float, bool]):
        return Filter(self.field_name, ">=", other)

    def __repr__(self):
        return "< {field_type} {field_name} >".format(field_type=self.__class__.__name__,
                                                      field_name=self.field_name)  # pragma: no cover


class AnyField(BaseField):
    pass


class BooleanField(BaseField):

    def check_type(self, value):
        return isinstance(value, bool)


class IntField(BaseField):

    def check_type(self, value):
        return isinstance(value, int) and not isinstance(value, bool)

    @classmethod
    def _dumps(cls, value) -> int:
        return int(value)


class FloatField(BaseField):

    def check_type(self, value):
        return isinstance(value, float)

    @classmethod
    def _dumps(cls, value) -> float:
        return float(value)


class StringField(BaseField):

    def check_type(self, value):
        return isinstance(value, str)

    @classmethod
    def _dumps(cls, value) -> str:
        return str(value)


class DictField(BaseField):

    def check_type(self, value):
        return isinstance(value, dict)

    @classmethod
    def _dumps(cls, value) -> str:
        return json.dumps(value)

    def loads(self, serialized_value: str) -> dict:
        return json.loads(serialized_value)


class ListField(BaseField):
    def check_type(self, value):
        return isinstance(value, list)

    @classmethod
    def _dumps(cls, value) -> list:
        return json.dumps(value)

    def loads(self, serialized_value) -> list:
        return json.loads(serialized_value)

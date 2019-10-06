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

    def _generate_filter(self, op: str, other: Union[str, int, float, bool]):
        if self.enforce_type and not self.check_type(other):
            raise ValueError(
                "Comparing field {} with '{}' of type {}".format(self.__class__.__name__, other, type(other)))
        return Filter(self.field_name, op, other)

    def __eq__(self, other: Union[str, int, float, bool]):
        return self._generate_filter("=", other)

    def __lt__(self, other: Union[str, int, float, bool]):
        return self._generate_filter("<", other)

    def __gt__(self, other: Union[str, int, float, bool]):
        return self._generate_filter(">", other)

    def __le__(self, other: Union[str, int, float, bool]):
        return self._generate_filter("<=", other)

    def __ge__(self, other: Union[str, int, float, bool]):
        return self._generate_filter(">=", other)

    def __repr__(self):
        return "< {field_type} name={field_name} >".format(field_type=self.__class__.__name__,
                                                      field_name=self.field_name)  # pragma: no cover


class AnyField(BaseField):
    pass


class BooleanField(BaseField):

    def check_type(self, value):
        return isinstance(value, bool)

    @classmethod
    def _dumps(cls, value) -> bool:
        return bool(value)

    @property
    def default(self):
        return super().default or bool()


class IntField(BaseField):

    def check_type(self, value):
        return isinstance(value, int) and not isinstance(value, bool)

    @classmethod
    def _dumps(cls, value) -> int:
        return int(value)

    @property
    def default(self):
        return super().default or int()


class FloatField(BaseField):

    def check_type(self, value):
        return isinstance(value, float)

    @classmethod
    def _dumps(cls, value) -> float:
        return float(value)

    @property
    def default(self):
        return super().default or float()


class StringField(BaseField):

    def check_type(self, value):
        return isinstance(value, str)

    @classmethod
    def _dumps(cls, value) -> str:
        return str(value)

    @property
    def default(self):
        return super().default or str()


class JSONField(BaseField):
    def check_type(self, value):
        json_types = [bool, int, float, str, list, dict]
        return any(isinstance(value, json_type) for json_type in json_types)

    @classmethod
    def _dumps(cls, value) -> str:
        return json.dumps(value)

    def loads(self, serialized_value: str) -> dict:
        return json.loads(serialized_value)

    @property
    def default(self):
        return super().default or dict()


class DictField(JSONField):

    def check_type(self, value):
        return isinstance(value, dict)


class ListField(JSONField):
    def check_type(self, value):
        return isinstance(value, list)

    @property
    def default(self):
        return super().default or list()

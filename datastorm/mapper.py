from typing import Any, Optional, Dict, List

from datastorm.fields import AnyField, BaseField


class FieldMapper:

    def __init__(self):
        self.__mappings: Dict[str, BaseField] = {}

    def get_field(self, field_name: str) -> BaseField:
        return self.__mappings.get(field_name, AnyField())

    def set_field(self, field_name: str, field: BaseField):
        field.field_name = field.field_name or field_name
        self.__mappings[field_name] = field

    def default(self, field_name: str) -> Any:
        return self.__mappings[field_name].default

    def dumps(self, field_name: str, value: Any, field: Optional[BaseField] = None) -> Any:
        field = field or self.get_field(field_name)
        return field.dumps(value)

    def loads(self, field_name: str, value: Any, field: Optional[BaseField] = None) -> Any:
        field = field or self.get_field(field_name)
        return field.loads(value)

    @property
    def fields(self) -> List[str]:
        return list(self.__mappings)

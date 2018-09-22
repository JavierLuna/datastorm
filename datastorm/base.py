from typing import Any


class FieldABC:
    default = lambda : NotImplementedError

    def loads(self, serialized_value: Any) -> Any:
        raise NotImplementedError  # pragma: no cover

    def dumps(self, value: Any) -> Any:
        raise NotImplementedError  # pragma: no cover

    def check_type(self, value) -> bool:
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: Any):
        raise NotImplementedError  # pragma: no cover

    def __lt__(self, other: Any):
        raise NotImplementedError  # pragma: no cover

    def __gt__(self, other: Any):
        raise NotImplementedError  # pragma: no cover

    def __le__(self, other: Any):
        raise NotImplementedError  # pragma: no cover

    def __ge__(self, other: Any):
        raise NotImplementedError  # pragma: no cover

    def __repr__(self):
        raise NotImplementedError  # pragma: no cover
from __future__ import annotations
from typing import TypeVar, Type

T = TypeVar("T")  # pylint: disable=C0103


def eq(cls: Type[T]) -> Type[T]:
    """Class decorator providing generic comparison functionality."""
    def __eq__(self: T, other: object) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
    cls.__eq__ = __eq__  # type: ignore
    return cls

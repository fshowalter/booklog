"""Custom types for the repository layer."""

from collections.abc import Sequence
from typing import TypeVar, overload

T = TypeVar("T")


class NonEmptyList[T](list[T]):
    """A list that must contain at least one element.

    This type ensures at compile-time that lists cannot be empty,
    eliminating the need for runtime empty checks.
    """

    @overload
    def __init__(self, first: T, /) -> None: ...

    @overload
    def __init__(self, first: T, /, *rest: T) -> None: ...

    def __init__(self, first: T, /, *rest: T) -> None:
        """Initialize with at least one required element."""
        super().__init__([first, *rest])

    @classmethod
    def from_sequence(cls, seq: Sequence[T]) -> "NonEmptyList[T]":
        """Create from a sequence, raising ValueError if empty."""
        if not seq:
            raise ValueError("Cannot create NonEmptyList from empty sequence")
        first, *rest = seq
        return cls(first, *rest)

    def __bool__(self) -> bool:
        """NonEmptyList is always truthy."""
        return True

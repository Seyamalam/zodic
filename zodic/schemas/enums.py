"""Enum schema types for Zodic."""

from typing import Any, List, TypeVar, Union
from ..core.base import Schema
from ..core.types import ValidationContext
from ..core.errors import ZodError, custom_issue

T = TypeVar("T")


class EnumSchema(Schema[T]):
    """Schema for enum validation."""

    def __init__(self, values: List[T]) -> None:
        super().__init__()
        self.values = values

    def _parse_value(self, value: Any, ctx: ValidationContext) -> T:
        """Parse and validate an enum value."""
        if value not in self.values:
            values_str = ", ".join(repr(v) for v in self.values)
            raise ZodError(
                [
                    custom_issue(
                        f"Expected one of [{values_str}], received {repr(value)}",
                        ctx,
                        value,
                    )
                ]
            )
        return value

    def _clone(self) -> "EnumSchema[T]":
        """Create a copy of this schema."""
        new_schema = super()._clone()
        new_schema.values = self.values.copy()
        return new_schema


def enum(values: List[T]) -> EnumSchema[T]:
    """Create an enum schema."""
    return EnumSchema(values)

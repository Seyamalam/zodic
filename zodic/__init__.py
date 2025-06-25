"""
Zodic - A TypeScript Zod-inspired validation library for Python.

Zodic provides a simple, chainable API for validating and parsing data
with excellent type safety and developer experience.

Example:
    >>> import zodic as z
    >>> schema = z.string().min(3).max(10)
    >>> result = schema.parse("hello")  # Returns "hello"
    >>> 
    >>> user_schema = z.object({
    ...     'name': z.string(),
    ...     'age': z.number().int().positive()
    ... })
    >>> user = user_schema.parse({'name': 'John', 'age': 30})
"""

__version__ = "0.2.0"
__author__ = "Touhidul Alam Seyam"
__email__ = "seyamalam41@gmail.com"

from .core.base import Schema
from .core.errors import ZodError, ValidationError
from .schemas.primitives import (
    string,
    number,
    boolean,
    none,
    literal,
    date_schema,
    datetime_schema,
)

# Convenience aliases
date = date_schema
datetime = datetime_schema
from .schemas.collections import object, array
from .schemas.special import optional, nullable, union
from .schemas.enums import enum

# Main API exports - following Zod's naming convention
__all__ = [
    # Core classes
    "Schema",
    "ZodError",
    "ValidationError",
    # Schema constructors
    "string",
    "number",
    "boolean",
    "none",
    "literal",
    "date_schema",
    "datetime_schema",
    "date",
    "datetime",
    "object",
    "array",
    "enum",
    "optional",
    "nullable",
    "union",
    # Version info
    "__version__",
]

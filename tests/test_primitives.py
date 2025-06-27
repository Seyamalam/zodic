"""Tests for primitive type schemas."""

import os
import sys

import pytest

import zodic as z
from zodic import ZodError

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestStringSchema:
    """Tests for StringSchema."""

    def test_valid_string(self):
        """Test parsing valid strings."""
        schema = z.string()
        assert schema.parse("hello") == "hello"
        assert schema.parse("") == ""
        assert schema.parse("123") == "123"

    def test_invalid_type(self):
        """Test parsing invalid types."""
        schema = z.string()

        with pytest.raises(ZodError) as exc_info:
            schema.parse(123)
        assert "Expected string, received int" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse(None)

        with pytest.raises(ZodError):
            schema.parse([])

    def test_safe_parse_success(self):
        """Test safe_parse with valid input."""
        schema = z.string()
        result = schema.safe_parse("hello")

        assert result["success"] is True
        assert result["data"] == "hello"

    def test_safe_parse_failure(self):
        """Test safe_parse with invalid input."""
        schema = z.string()
        result = schema.safe_parse(123)

        assert result["success"] is False
        assert isinstance(result["error"], ZodError)

    def test_min_length(self):
        """Test minimum length constraint."""
        schema = z.string().min(3)

        assert schema.parse("hello") == "hello"
        assert schema.parse("abc") == "abc"

        with pytest.raises(ZodError) as exc_info:
            schema.parse("hi")
        assert "at least 3 characters" in str(exc_info.value)

    def test_max_length(self):
        """Test maximum length constraint."""
        schema = z.string().max(5)

        assert schema.parse("hello") == "hello"
        assert schema.parse("hi") == "hi"

        with pytest.raises(ZodError) as exc_info:
            schema.parse("toolong")
        assert "at most 5 characters" in str(exc_info.value)

    def test_exact_length(self):
        """Test exact length constraint."""
        schema = z.string().length(5)

        assert schema.parse("hello") == "hello"

        with pytest.raises(ZodError):
            schema.parse("hi")

        with pytest.raises(ZodError):
            schema.parse("toolong")

    def test_chained_constraints(self):
        """Test chaining multiple constraints."""
        schema = z.string().min(2).max(10)

        assert schema.parse("hello") == "hello"

        with pytest.raises(ZodError):
            schema.parse("a")

        with pytest.raises(ZodError):
            schema.parse("verylongstring")


class TestNumberSchema:
    """Tests for NumberSchema."""

    def test_valid_numbers(self):
        """Test parsing valid numbers."""
        schema = z.number()

        assert schema.parse(42) == 42
        assert schema.parse(3.14) == 3.14
        assert schema.parse(0) == 0
        assert schema.parse(-5) == -5

    def test_invalid_type(self):
        """Test parsing invalid types."""
        schema = z.number()

        with pytest.raises(ZodError) as exc_info:
            schema.parse("123")
        assert "Expected number, received str" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse(None)

        with pytest.raises(ZodError):
            schema.parse([])

    def test_nan_and_infinity(self):
        """Test handling of NaN and infinity."""
        schema = z.number()

        with pytest.raises(ZodError) as exc_info:
            schema.parse(float("nan"))
        assert "cannot be NaN" in str(exc_info.value)

        with pytest.raises(ZodError) as exc_info:
            schema.parse(float("inf"))
        assert "cannot be infinite" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse(float("-inf"))

    def test_integer_constraint(self):
        """Test integer-only constraint."""
        schema = z.number().int()

        assert schema.parse(42) == 42
        assert schema.parse(0) == 0
        assert schema.parse(-5) == -5

        # Float that is actually an integer should be converted
        assert schema.parse(42.0) == 42

        with pytest.raises(ZodError) as exc_info:
            schema.parse(3.14)
        assert "Expected integer" in str(exc_info.value)

    def test_min_value(self):
        """Test minimum value constraint."""
        schema = z.number().min(0)

        assert schema.parse(5) == 5
        assert schema.parse(0) == 0

        with pytest.raises(ZodError) as exc_info:
            schema.parse(-1)
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_max_value(self):
        """Test maximum value constraint."""
        schema = z.number().max(100)

        assert schema.parse(50) == 50
        assert schema.parse(100) == 100

        with pytest.raises(ZodError) as exc_info:
            schema.parse(101)
        assert "less than or equal to 100" in str(exc_info.value)

    def test_positive(self):
        """Test positive constraint."""
        schema = z.number().positive()

        assert schema.parse(1) == 1
        assert schema.parse(0.1) == 0.1

        with pytest.raises(ZodError):
            schema.parse(0)

        with pytest.raises(ZodError):
            schema.parse(-1)

    def test_negative(self):
        """Test negative constraint."""
        schema = z.number().negative()

        assert schema.parse(-1) == -1
        assert schema.parse(-0.1) == -0.1

        with pytest.raises(ZodError):
            schema.parse(0)

        with pytest.raises(ZodError):
            schema.parse(1)

    def test_nonnegative(self):
        """Test non-negative constraint."""
        schema = z.number().nonnegative()

        assert schema.parse(0) == 0
        assert schema.parse(1) == 1
        assert schema.parse(0.1) == 0.1

        with pytest.raises(ZodError):
            schema.parse(-1)

    def test_chained_constraints(self):
        """Test chaining multiple constraints."""
        schema = z.number().int().min(0).max(100)

        assert schema.parse(50) == 50
        assert schema.parse(0) == 0
        assert schema.parse(100) == 100

        with pytest.raises(ZodError):
            schema.parse(-1)

        with pytest.raises(ZodError):
            schema.parse(101)

        with pytest.raises(ZodError):
            schema.parse(50.5)


class TestBooleanSchema:
    """Tests for BooleanSchema."""

    def test_valid_booleans(self):
        """Test parsing valid booleans."""
        schema = z.boolean()

        assert schema.parse(True) is True
        assert schema.parse(False) is False

    def test_invalid_type(self):
        """Test parsing invalid types."""
        schema = z.boolean()

        with pytest.raises(ZodError) as exc_info:
            schema.parse(1)
        assert "Expected boolean, received int" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse("true")

        with pytest.raises(ZodError):
            schema.parse(None)


class TestNoneSchema:
    """Tests for NoneSchema."""

    def test_valid_none(self):
        """Test parsing valid None."""
        schema = z.none()

        assert schema.parse(None) is None

    def test_invalid_type(self):
        """Test parsing invalid types."""
        schema = z.none()

        with pytest.raises(ZodError) as exc_info:
            schema.parse("null")
        assert "Expected null, received str" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse(0)

        with pytest.raises(ZodError):
            schema.parse(False)

"""Tests for base schema features like transforms, refinements, etc."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import zodic as z
from zodic import ZodError


class TestTransforms:
    """Tests for transform functionality."""

    def test_string_transform(self):
        """Test string transformation."""
        schema = z.string().transform(str.upper)

        result = schema.parse("hello")
        assert result == "HELLO"

    def test_number_transform(self):
        """Test number transformation."""
        schema = z.number().transform(lambda x: x * 2)

        result = schema.parse(5)
        assert result == 10

    def test_chained_transforms(self):
        """Test chaining multiple transforms."""
        schema = z.string().transform(str.strip).transform(str.upper)

        result = schema.parse("  hello  ")
        assert result == "HELLO"

    def test_transform_with_validation(self):
        """Test transform combined with validation."""
        schema = z.string().min(3).transform(str.upper)

        result = schema.parse("hello")
        assert result == "HELLO"

        # Validation happens before transform
        with pytest.raises(ZodError):
            schema.parse("hi")


class TestRefinements:
    """Tests for refinement functionality."""

    def test_string_refinement(self):
        """Test string refinement."""
        schema = z.string().refine(
            lambda x: x.startswith("hello"), "String must start with 'hello'"
        )

        assert schema.parse("hello world") == "hello world"

        with pytest.raises(ZodError) as exc_info:
            schema.parse("hi there")
        assert "String must start with 'hello'" in str(exc_info.value)

    def test_number_refinement(self):
        """Test number refinement."""
        schema = z.number().refine(lambda x: x % 2 == 0, "Number must be even")

        assert schema.parse(4) == 4
        assert schema.parse(0) == 0

        with pytest.raises(ZodError) as exc_info:
            schema.parse(3)
        assert "Number must be even" in str(exc_info.value)

    def test_multiple_refinements(self):
        """Test multiple refinements."""
        schema = (
            z.number()
            .refine(lambda x: x > 0, "Must be positive")
            .refine(lambda x: x % 2 == 0, "Must be even")
        )

        assert schema.parse(4) == 4

        with pytest.raises(ZodError) as exc_info:
            schema.parse(-2)
        assert "Must be positive" in str(exc_info.value)

        with pytest.raises(ZodError) as exc_info:
            schema.parse(3)
        assert "Must be even" in str(exc_info.value)

    def test_refinement_with_transform(self):
        """Test refinement combined with transform."""
        schema = (
            z.string()
            .transform(str.strip)
            .refine(lambda x: len(x) > 0, "Cannot be empty after trimming")
        )

        assert schema.parse("  hello  ") == "hello"

        with pytest.raises(ZodError) as exc_info:
            schema.parse("   ")
        assert "Cannot be empty after trimming" in str(exc_info.value)


class TestOptionalAndNullable:
    """Tests for optional and nullable functionality."""

    def test_optional_schema(self):
        """Test optional schema."""
        schema = z.string().optional()

        assert schema.parse("hello") == "hello"
        assert schema.parse(None) is None

        # Test with safe_parse
        result = schema.safe_parse(None)
        assert result["success"] is True
        assert result["data"] is None

    def test_nullable_schema(self):
        """Test nullable schema."""
        schema = z.string().nullable()

        assert schema.parse("hello") == "hello"
        assert schema.parse(None) is None

        # Still validates type when not None
        with pytest.raises(ZodError):
            schema.parse(123)

    def test_optional_with_default(self):
        """Test optional schema with default value."""
        schema = z.string().default("default_value")

        assert schema.parse("hello") == "hello"

        # Test with missing value (simulated)
        from zodic.core.base import UNDEFINED

        result = schema.safe_parse(UNDEFINED)
        assert result["success"] is True
        assert result["data"] == "default_value"

    def test_chaining_optional_nullable(self):
        """Test chaining optional and nullable."""
        schema = z.string().optional().nullable()

        assert schema.parse("hello") == "hello"
        assert schema.parse(None) is None

        # Test with safe_parse for undefined
        from zodic.core.base import UNDEFINED

        result = schema.safe_parse(UNDEFINED)
        assert result["success"] is True
        assert result["data"] is None


class TestErrorHandling:
    """Tests for error handling and formatting."""

    def test_error_message_format(self):
        """Test error message formatting."""
        schema = z.string()

        try:
            schema.parse(123)
        except ZodError as e:
            assert "Expected string, received int" in str(e)
            assert len(e.issues) == 1
            assert e.issues[0]["code"] == "invalid_type"

    def test_error_flatten(self):
        """Test error flattening."""
        schema = z.string()

        try:
            schema.parse(123)
        except ZodError as e:
            flattened = e.flatten()
            assert "root" in flattened
            assert len(flattened["root"]) == 1

    def test_error_format(self):
        """Test error formatting."""
        schema = z.string()

        try:
            schema.parse(123)
        except ZodError as e:
            formatted = e.format()
            assert len(formatted) == 1
            assert formatted[0]["code"] == "invalid_type"
            assert formatted[0]["received"] == 123
            assert formatted[0]["expected"] == "string"

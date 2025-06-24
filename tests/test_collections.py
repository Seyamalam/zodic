"""Tests for collection type schemas."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import zodic as z
from zodic import ZodError


class TestObjectSchema:
    """Tests for ObjectSchema."""

    def test_valid_object(self):
        """Test parsing valid objects."""
        schema = z.object(
            {"name": z.string(), "age": z.number().int(), "active": z.boolean()}
        )

        data = {"name": "John", "age": 30, "active": True}

        result = schema.parse(data)
        assert result == data

    def test_invalid_type(self):
        """Test parsing invalid types."""
        schema = z.object({"name": z.string()})

        with pytest.raises(ZodError) as exc_info:
            schema.parse("not an object")
        assert "Expected object, received str" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse([])

        with pytest.raises(ZodError):
            schema.parse(None)

    def test_missing_required_field(self):
        """Test missing required fields."""
        schema = z.object({"name": z.string(), "age": z.number()})

        with pytest.raises(ZodError) as exc_info:
            schema.parse({"name": "John"})
        assert "Required" in str(exc_info.value)

    def test_invalid_field_type(self):
        """Test invalid field types."""
        schema = z.object({"name": z.string(), "age": z.number()})

        with pytest.raises(ZodError) as exc_info:
            schema.parse({"name": "John", "age": "thirty"})
        assert "age" in str(exc_info.value)
        assert "Expected number, received str" in str(exc_info.value)

    def test_optional_fields(self):
        """Test optional fields."""
        schema = z.object({"name": z.string(), "age": z.number().optional()})

        # With optional field
        result1 = schema.parse({"name": "John", "age": 30})
        assert result1 == {"name": "John", "age": 30}

        # Without optional field
        result2 = schema.parse({"name": "John"})
        assert result2 == {"name": "John"}

    def test_default_values(self):
        """Test default values."""
        schema = z.object({"name": z.string(), "active": z.boolean().default(True)})

        # With explicit value
        result1 = schema.parse({"name": "John", "active": False})
        assert result1 == {"name": "John", "active": False}

        # With default value
        result2 = schema.parse({"name": "John"})
        assert result2 == {"name": "John", "active": True}

    def test_unknown_keys_strip(self):
        """Test stripping unknown keys (default behavior)."""
        schema = z.object({"name": z.string()})

        data = {"name": "John", "unknown": "value"}
        result = schema.parse(data)

        assert result == {"name": "John"}
        assert "unknown" not in result

    def test_unknown_keys_strict(self):
        """Test strict mode with unknown keys."""
        schema = z.object({"name": z.string()}).strict()

        with pytest.raises(ZodError) as exc_info:
            schema.parse({"name": "John", "unknown": "value"})
        assert "Unrecognized key: unknown" in str(exc_info.value)

    def test_unknown_keys_passthrough(self):
        """Test passthrough mode with unknown keys."""
        schema = z.object({"name": z.string()}).passthrough()

        data = {"name": "John", "unknown": "value"}
        result = schema.parse(data)

        assert result == {"name": "John", "unknown": "value"}

    def test_nested_objects(self):
        """Test nested object validation."""
        schema = z.object(
            {
                "user": z.object({"name": z.string(), "age": z.number()}),
                "active": z.boolean(),
            }
        )

        data = {"user": {"name": "John", "age": 30}, "active": True}

        result = schema.parse(data)
        assert result == data

        # Test nested validation error
        with pytest.raises(ZodError) as exc_info:
            schema.parse({"user": {"name": "John", "age": "thirty"}, "active": True})
        assert "user.age" in str(exc_info.value)


class TestArraySchema:
    """Tests for ArraySchema."""

    def test_valid_array(self):
        """Test parsing valid arrays."""
        schema = z.array(z.string())

        result = schema.parse(["hello", "world"])
        assert result == ["hello", "world"]

        # Empty array
        result = schema.parse([])
        assert result == []

    def test_invalid_type(self):
        """Test parsing invalid types."""
        schema = z.array(z.string())

        with pytest.raises(ZodError) as exc_info:
            schema.parse("not an array")
        assert "Expected array, received str" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse({})

        with pytest.raises(ZodError):
            schema.parse(None)

    def test_invalid_element_type(self):
        """Test invalid element types."""
        schema = z.array(z.string())

        with pytest.raises(ZodError) as exc_info:
            schema.parse(["hello", 123, "world"])
        assert "[1]" in str(exc_info.value)  # Index 1 in error path
        assert "Expected string, received int" in str(exc_info.value)

    def test_min_length(self):
        """Test minimum length constraint."""
        schema = z.array(z.string()).min(2)

        assert schema.parse(["a", "b"]) == ["a", "b"]
        assert schema.parse(["a", "b", "c"]) == ["a", "b", "c"]

        with pytest.raises(ZodError) as exc_info:
            schema.parse(["a"])
        assert "at least 2 elements" in str(exc_info.value)

    def test_max_length(self):
        """Test maximum length constraint."""
        schema = z.array(z.string()).max(2)

        assert schema.parse(["a"]) == ["a"]
        assert schema.parse(["a", "b"]) == ["a", "b"]

        with pytest.raises(ZodError) as exc_info:
            schema.parse(["a", "b", "c"])
        assert "at most 2 elements" in str(exc_info.value)

    def test_exact_length(self):
        """Test exact length constraint."""
        schema = z.array(z.string()).length(2)

        assert schema.parse(["a", "b"]) == ["a", "b"]

        with pytest.raises(ZodError):
            schema.parse(["a"])

        with pytest.raises(ZodError):
            schema.parse(["a", "b", "c"])

    def test_nonempty(self):
        """Test non-empty constraint."""
        schema = z.array(z.string()).nonempty()

        assert schema.parse(["a"]) == ["a"]
        assert schema.parse(["a", "b"]) == ["a", "b"]

        with pytest.raises(ZodError) as exc_info:
            schema.parse([])
        assert "at least 1 elements" in str(exc_info.value)

    def test_nested_arrays(self):
        """Test nested array validation."""
        schema = z.array(z.array(z.number()))

        data = [[1, 2], [3, 4, 5], []]
        result = schema.parse(data)
        assert result == data

        # Test nested validation error
        with pytest.raises(ZodError) as exc_info:
            schema.parse([[1, 2], ["invalid"], [3]])
        assert "[1][0]" in str(exc_info.value)  # Path to nested error

    def test_array_of_objects(self):
        """Test array of objects."""
        schema = z.array(z.object({"name": z.string(), "age": z.number()}))

        data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]

        result = schema.parse(data)
        assert result == data

        # Test validation error in object element
        with pytest.raises(ZodError) as exc_info:
            schema.parse(
                [{"name": "John", "age": 30}, {"name": "Jane", "age": "twenty-five"}]
            )
        assert "[1].age" in str(exc_info.value)

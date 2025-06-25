"""Tests for new features added in v0.2.0."""

import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import zodic as z
from zodic import ZodError


class TestLiteralSchema:
    """Tests for LiteralSchema."""

    def test_valid_literal(self):
        """Test parsing valid literal values."""
        schema = z.literal("hello")
        assert schema.parse("hello") == "hello"

        number_schema = z.literal(42)
        assert number_schema.parse(42) == 42

        bool_schema = z.literal(True)
        assert bool_schema.parse(True) is True

    def test_invalid_literal(self):
        """Test parsing invalid literal values."""
        schema = z.literal("hello")

        with pytest.raises(ZodError) as exc_info:
            schema.parse("world")
        assert "Expected literal value 'hello'" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse(123)


class TestEnumSchema:
    """Tests for EnumSchema."""

    def test_valid_enum(self):
        """Test parsing valid enum values."""
        schema = z.enum(["red", "green", "blue"])
        assert schema.parse("red") == "red"
        assert schema.parse("green") == "green"
        assert schema.parse("blue") == "blue"

    def test_invalid_enum(self):
        """Test parsing invalid enum values."""
        schema = z.enum(["red", "green", "blue"])

        with pytest.raises(ZodError) as exc_info:
            schema.parse("yellow")
        assert "Expected one of ['red', 'green', 'blue']" in str(exc_info.value)

    def test_number_enum(self):
        """Test enum with numbers."""
        schema = z.enum([1, 2, 3])
        assert schema.parse(1) == 1
        assert schema.parse(2) == 2

        with pytest.raises(ZodError):
            schema.parse(4)


class TestStringValidation:
    """Tests for enhanced string validation."""

    def test_email_validation(self):
        """Test email validation."""
        schema = z.string().email()

        # Valid emails
        assert schema.parse("test@example.com") == "test@example.com"
        assert (
            schema.parse("user.name+tag@domain.co.uk") == "user.name+tag@domain.co.uk"
        )

        # Invalid emails
        with pytest.raises(ZodError) as exc_info:
            schema.parse("invalid-email")
        assert "Invalid email format" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse("@example.com")

        with pytest.raises(ZodError):
            schema.parse("test@")

    def test_url_validation(self):
        """Test URL validation."""
        schema = z.string().url()

        # Valid URLs
        assert schema.parse("https://example.com") == "https://example.com"
        assert schema.parse("http://localhost:8000") == "http://localhost:8000"
        assert (
            schema.parse("https://sub.domain.com/path?query=1")
            == "https://sub.domain.com/path?query=1"
        )

        # Invalid URLs
        with pytest.raises(ZodError) as exc_info:
            schema.parse("not-a-url")
        assert "Invalid URL format" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse("ftp://example.com")  # Only http/https supported

    def test_regex_validation(self):
        """Test regex pattern validation."""
        schema = z.string().regex(r"^[A-Z]{2,3}$")

        # Valid patterns
        assert schema.parse("AB") == "AB"
        assert schema.parse("XYZ") == "XYZ"

        # Invalid patterns
        with pytest.raises(ZodError) as exc_info:
            schema.parse("abc")
        assert "does not match pattern" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse("ABCD")

    def test_chained_string_validation(self):
        """Test chaining multiple string validations."""
        schema = z.string().min(5).max(50).email()

        assert schema.parse("test@example.com") == "test@example.com"

        # Too short
        with pytest.raises(ZodError):
            schema.parse("a@b.c")

        # Not an email
        with pytest.raises(ZodError):
            schema.parse("this-is-not-an-email")


class TestNumberValidation:
    """Tests for enhanced number validation."""

    def test_positive_validation_fixed(self):
        """Test that positive validation is fixed."""
        schema = z.number().positive()

        # Valid positive numbers
        assert schema.parse(1) == 1
        assert schema.parse(0.1) == 0.1
        assert schema.parse(100) == 100

        # Invalid: zero and negative
        with pytest.raises(ZodError) as exc_info:
            schema.parse(0)
        assert "Number must be positive" in str(exc_info.value)

        with pytest.raises(ZodError):
            schema.parse(-1)

    def test_positive_with_other_constraints(self):
        """Test positive validation with other constraints."""
        schema = z.number().int().positive().max(100)

        assert schema.parse(50) == 50

        # Not positive
        with pytest.raises(ZodError):
            schema.parse(0)

        # Too large
        with pytest.raises(ZodError):
            schema.parse(150)


class TestDateSchema:
    """Tests for DateSchema."""

    def test_date_object_parsing(self):
        """Test parsing date objects."""
        schema = z.date()
        test_date = date(2023, 12, 25)

        assert schema.parse(test_date) == test_date

    def test_datetime_to_date_conversion(self):
        """Test converting datetime to date."""
        schema = z.date()
        test_datetime = datetime(2023, 12, 25, 10, 30, 0)
        expected_date = date(2023, 12, 25)

        assert schema.parse(test_datetime) == expected_date

    def test_string_date_parsing(self):
        """Test parsing date strings."""
        schema = z.date()

        # ISO format
        assert schema.parse("2023-12-25") == date(2023, 12, 25)

        # Common formats
        assert schema.parse("12/25/2023") == date(2023, 12, 25)
        assert schema.parse("25/12/2023") == date(2023, 12, 25)

    def test_invalid_date_string(self):
        """Test invalid date strings."""
        schema = z.date()

        with pytest.raises(ZodError) as exc_info:
            schema.parse("not-a-date")
        assert "Invalid date format" in str(exc_info.value)

    def test_date_range_validation(self):
        """Test date range validation."""
        min_date = date(2023, 1, 1)
        max_date = date(2023, 12, 31)
        schema = z.date().min(min_date).max(max_date)

        # Valid date
        assert schema.parse("2023-06-15") == date(2023, 6, 15)

        # Too early
        with pytest.raises(ZodError) as exc_info:
            schema.parse("2022-12-31")
        assert "Date must be after" in str(exc_info.value)

        # Too late
        with pytest.raises(ZodError):
            schema.parse("2024-01-01")


class TestDateTimeSchema:
    """Tests for DateTimeSchema."""

    def test_datetime_object_parsing(self):
        """Test parsing datetime objects."""
        schema = z.datetime()
        test_datetime = datetime(2023, 12, 25, 10, 30, 0)

        assert schema.parse(test_datetime) == test_datetime

    def test_string_datetime_parsing(self):
        """Test parsing datetime strings."""
        schema = z.datetime()

        # ISO format
        result = schema.parse("2023-12-25T10:30:00")
        assert result == datetime(2023, 12, 25, 10, 30, 0)

        # With timezone
        result = schema.parse("2023-12-25T10:30:00+00:00")
        assert result == datetime(2023, 12, 25, 10, 30, 0)

    def test_invalid_datetime_string(self):
        """Test invalid datetime strings."""
        schema = z.datetime()

        with pytest.raises(ZodError) as exc_info:
            schema.parse("not-a-datetime")
        assert "Invalid datetime format" in str(exc_info.value)

    def test_datetime_range_validation(self):
        """Test datetime range validation."""
        min_datetime = datetime(2023, 1, 1, 0, 0, 0)
        max_datetime = datetime(2023, 12, 31, 23, 59, 59)
        schema = z.datetime().min(min_datetime).max(max_datetime)

        # Valid datetime
        result = schema.parse("2023-06-15T12:00:00")
        assert result == datetime(2023, 6, 15, 12, 0, 0)

        # Too early
        with pytest.raises(ZodError):
            schema.parse("2022-12-31T23:59:59")

        # Too late
        with pytest.raises(ZodError):
            schema.parse("2024-01-01T00:00:00")


class TestUnionOperator:
    """Tests for union operator (|)."""

    def test_union_operator(self):
        """Test union operator syntax."""
        schema = z.string() | z.number()

        assert schema.parse("hello") == "hello"
        assert schema.parse(42) == 42

        with pytest.raises(ZodError):
            schema.parse(True)

    def test_complex_union(self):
        """Test complex union with multiple types."""
        schema = z.string().email() | z.number().positive() | z.literal("admin")

        assert schema.parse("test@example.com") == "test@example.com"
        assert schema.parse(42) == 42
        assert schema.parse("admin") == "admin"

        with pytest.raises(ZodError):
            schema.parse("invalid-email")


class TestErrorHandling:
    """Tests for improved error handling."""

    def test_nested_error_paths(self):
        """Test that error paths are correctly maintained."""
        schema = z.object(
            {
                "user": z.object(
                    {"email": z.string().email(), "age": z.number().positive()}
                )
            }
        )

        try:
            schema.parse({"user": {"email": "invalid-email", "age": -5}})
        except ZodError as e:
            errors = e.flatten()
            assert "user.email" in errors
            assert "user.age" in errors

    def test_multiple_validation_errors(self):
        """Test multiple validation errors in one field."""
        schema = z.string().min(5).max(10).email()

        try:
            schema.parse("ab")  # Too short and not email
        except ZodError as e:
            # Should catch the first error (min length)
            assert "at least 5 characters" in str(e)

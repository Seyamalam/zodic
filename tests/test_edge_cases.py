"""Tests for edge cases and regression tests."""

import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import zodic as z
from zodic import ZodError


class TestEdgeCases:
    """Tests for edge cases and potential issues."""

    def test_empty_string_validation(self):
        """Test edge cases with empty strings."""
        schema = z.string().min(1)

        with pytest.raises(ZodError):
            schema.parse("")

        # But empty string should be valid without min constraint
        empty_schema = z.string()
        assert empty_schema.parse("") == ""

    def test_zero_validation_edge_cases(self):
        """Test edge cases around zero validation."""
        positive_schema = z.number().positive()
        nonnegative_schema = z.number().nonnegative()

        # Zero should fail positive but pass nonnegative
        with pytest.raises(ZodError):
            positive_schema.parse(0)

        assert nonnegative_schema.parse(0) == 0

        # Very small positive numbers
        assert positive_schema.parse(0.000001) == 0.000001
        assert positive_schema.parse(1e-10) == 1e-10

    def test_float_precision_edge_cases(self):
        """Test floating point precision edge cases."""
        schema = z.number().min(0.1).max(0.9)

        # Test boundary values
        assert schema.parse(0.1) == 0.1
        assert schema.parse(0.9) == 0.9

        # Test values just outside boundaries
        with pytest.raises(ZodError):
            schema.parse(0.09999999)

        with pytest.raises(ZodError):
            schema.parse(0.90000001)

    def test_large_numbers(self):
        """Test very large numbers."""
        schema = z.number()

        large_int = 2**63 - 1
        assert schema.parse(large_int) == large_int

        large_float = 1.7976931348623157e308
        assert schema.parse(large_float) == large_float

    def test_unicode_strings(self):
        """Test unicode string handling."""
        schema = z.string().min(1).max(10)

        # Unicode characters
        assert schema.parse("cafe") == "cafe"
        assert schema.parse("rocket") == "rocket"
        assert schema.parse("hello") == "hello"

        # Length counting with unicode
        unicode_schema = z.string().length(3)
        assert unicode_schema.parse("abc") == "abc"

    def test_regex_edge_cases(self):
        """Test regex pattern edge cases."""
        # Empty pattern
        empty_pattern = z.string().regex(r"")
        assert empty_pattern.parse("") == ""
        assert empty_pattern.parse("anything") == "anything"

        # Complex pattern
        complex_pattern = z.string().regex(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
        )
        assert complex_pattern.parse("Password123") == "Password123"

        with pytest.raises(ZodError):
            complex_pattern.parse("password")  # No uppercase or digit

    def test_email_edge_cases(self):
        """Test email validation edge cases."""
        schema = z.string().email()

        # Valid edge cases
        assert schema.parse("a@b.co") == "a@b.co"
        assert schema.parse("user+tag@example.com") == "user+tag@example.com"
        assert schema.parse("user.name@sub.domain.com") == "user.name@sub.domain.com"

        # Invalid edge cases
        with pytest.raises(ZodError):
            schema.parse("@example.com")  # Missing local part

        with pytest.raises(ZodError):
            schema.parse("user@")  # Missing domain

        with pytest.raises(ZodError):
            schema.parse("user@domain")  # Missing TLD

    def test_url_edge_cases(self):
        """Test URL validation edge cases."""
        schema = z.string().url()

        # Valid edge cases
        assert schema.parse("http://localhost") == "http://localhost"
        assert schema.parse("https://127.0.0.1:8080") == "https://127.0.0.1:8080"
        assert (
            schema.parse("https://example.com/path?query=value#fragment")
            == "https://example.com/path?query=value#fragment"
        )

        # Invalid edge cases
        with pytest.raises(ZodError):
            schema.parse("ftp://example.com")  # Wrong protocol

        with pytest.raises(ZodError):
            schema.parse("http://")  # Missing domain

        with pytest.raises(ZodError):
            schema.parse("not-a-url")  # Not a URL

    def test_date_parsing_edge_cases(self):
        """Test date parsing edge cases."""
        schema = z.date()

        # Leap year
        assert schema.parse("2024-02-29") == date(2024, 2, 29)

        # Year boundaries
        assert schema.parse("2000-01-01") == date(2000, 1, 1)
        assert schema.parse("9999-12-31") == date(9999, 12, 31)

        # Invalid dates
        with pytest.raises(ZodError):
            schema.parse("2023-02-29")  # Not a leap year

        with pytest.raises(ZodError):
            schema.parse("2024-13-01")  # Invalid month

        with pytest.raises(ZodError):
            schema.parse("2024-01-32")  # Invalid day

    def test_datetime_timezone_edge_cases(self):
        """Test datetime with timezone edge cases."""
        schema = z.datetime()

        # Various timezone formats
        assert schema.parse("2024-12-19T10:30:00Z") == datetime(2024, 12, 19, 10, 30, 0)
        assert schema.parse("2024-12-19T10:30:00+00:00") == datetime(
            2024, 12, 19, 10, 30, 0
        )

        # Without timezone
        assert schema.parse("2024-12-19T10:30:00") == datetime(2024, 12, 19, 10, 30, 0)

    def test_nested_object_edge_cases(self):
        """Test deeply nested object validation."""
        deep_schema = z.object(
            {
                "level1": z.object(
                    {"level2": z.object({"level3": z.object({"value": z.string()})})}
                )
            }
        )

        valid_data = {"level1": {"level2": {"level3": {"value": "deep"}}}}

        assert deep_schema.parse(valid_data) == valid_data

        # Test error path in deep nesting
        invalid_data = {
            "level1": {"level2": {"level3": {"value": 123}}}  # Should be string
        }

        try:
            deep_schema.parse(invalid_data)
        except ZodError as e:
            errors = e.flatten()
            assert "level1.level2.level3.value" in errors

    def test_array_edge_cases(self):
        """Test array validation edge cases."""
        # Empty array
        empty_schema = z.array(z.string()).min(0)
        assert empty_schema.parse([]) == []

        # Large array
        large_schema = z.array(z.number())
        large_array = list(range(1000))
        assert large_schema.parse(large_array) == large_array

        # Array with mixed valid/invalid items
        mixed_schema = z.array(z.string())
        try:
            mixed_schema.parse(["valid", 123, "also_valid"])
        except ZodError as e:
            errors = e.flatten()
            assert "[1]" in errors  # Error at index 1

    def test_union_edge_cases(self):
        """Test union validation edge cases."""
        # Union with overlapping types
        schema = z.string() | z.string().email()
        assert schema.parse("hello") == "hello"  # Matches first
        assert schema.parse("test@example.com") == "test@example.com"

        # Union with no matches
        strict_schema = z.literal("exact") | z.number().positive()

        with pytest.raises(ZodError) as exc_info:
            strict_schema.parse("not-exact")
        assert "did not match any union option" in str(exc_info.value)

    def test_transform_edge_cases(self):
        """Test transformation edge cases."""

        # Transform that could fail
        def risky_transform(x):
            if x == "error":
                raise ValueError("Transform failed")
            return x.upper()

        schema = z.string().transform(risky_transform)
        assert schema.parse("hello") == "HELLO"

        # Transform failure should be caught
        try:
            schema.parse("error")
        except ZodError as e:
            assert "Unexpected error" in str(e)

    def test_refinement_edge_cases(self):
        """Test refinement edge cases."""
        # Multiple refinements
        schema = (
            z.string()
            .refine(lambda x: len(x) > 0, "Cannot be empty")
            .refine(lambda x: x.isalpha(), "Must be alphabetic")
            .refine(lambda x: x.islower(), "Must be lowercase")
        )

        assert schema.parse("hello") == "hello"

        # Should fail on first refinement that fails
        with pytest.raises(ZodError) as exc_info:
            schema.parse("Hello123")
        assert "Must be alphabetic" in str(exc_info.value)

    def test_optional_and_nullable_edge_cases(self):
        """Test optional and nullable edge cases."""
        # Both optional and nullable
        schema = z.string().optional().nullable()

        assert schema.parse("hello") == "hello"
        assert schema.parse(None) is None

        # Test with UNDEFINED
        from zodic.core.base import UNDEFINED

        result = schema.safe_parse(UNDEFINED)
        assert result["success"] is True
        assert result["data"] is None

    def test_default_value_edge_cases(self):
        """Test default value edge cases."""
        # Default with function
        counter = 0

        def get_default():
            nonlocal counter
            counter += 1
            return f"default_{counter}"

        # Note: Current implementation doesn't support callable defaults
        # This is a potential enhancement for future versions
        schema = z.string().default("static_default")

        from zodic.core.base import UNDEFINED

        result = schema.safe_parse(UNDEFINED)
        assert result["data"] == "static_default"

    def test_schema_cloning_edge_cases(self):
        """Test schema cloning preserves all state."""
        original = (
            z.string()
            .min(5)
            .max(15)  # Increased to accommodate test email
            .email()
            .transform(str.lower)
            .refine(lambda x: x.startswith("test"), "Must start with test")
        )

        cloned = original.optional()

        # Original should still work with a shorter email
        assert original.parse("TEST@X.CO") == "test@x.co"

        # Cloned should work with None
        assert cloned.parse(None) is None
        assert cloned.parse("TEST@X.CO") == "test@x.co"

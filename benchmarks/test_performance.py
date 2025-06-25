"""Performance benchmarks for Zodic."""

import pytest
import zodic as z


class TestStringPerformance:
    """Benchmark string validation performance."""
    
    def test_simple_string_validation(self, benchmark):
        """Benchmark simple string validation."""
        schema = z.string()
        result = benchmark(schema.parse, "hello world")
        assert result == "hello world"
    
    def test_string_with_constraints(self, benchmark):
        """Benchmark string validation with constraints."""
        schema = z.string().min(5).max(100)
        result = benchmark(schema.parse, "hello world")
        assert result == "hello world"
    
    def test_string_with_transform(self, benchmark):
        """Benchmark string validation with transformation."""
        schema = z.string().transform(str.upper)
        result = benchmark(schema.parse, "hello world")
        assert result == "HELLO WORLD"
    
    def test_string_with_refinement(self, benchmark):
        """Benchmark string validation with refinement."""
        schema = z.string().refine(lambda x: x.startswith("hello"))
        result = benchmark(schema.parse, "hello world")
        assert result == "hello world"


class TestNumberPerformance:
    """Benchmark number validation performance."""
    
    def test_simple_number_validation(self, benchmark):
        """Benchmark simple number validation."""
        schema = z.number()
        result = benchmark(schema.parse, 42)
        assert result == 42
    
    def test_number_with_constraints(self, benchmark):
        """Benchmark number validation with constraints."""
        schema = z.number().int().positive().min(1).max(100)
        result = benchmark(schema.parse, 42)
        assert result == 42
    
    def test_number_with_transform(self, benchmark):
        """Benchmark number validation with transformation."""
        schema = z.number().transform(lambda x: x * 2)
        result = benchmark(schema.parse, 21)
        assert result == 42


class TestObjectPerformance:
    """Benchmark object validation performance."""
    
    def test_simple_object_validation(self, benchmark):
        """Benchmark simple object validation."""
        schema = z.object({
            "name": z.string(),
            "age": z.number()
        })
        data = {"name": "John", "age": 30}
        result = benchmark(schema.parse, data)
        assert result == data
    
    def test_complex_object_validation(self, benchmark):
        """Benchmark complex object validation."""
        schema = z.object({
            "name": z.string().min(1).max(100),
            "age": z.number().int().positive(),
            "email": z.string().optional(),
            "address": z.object({
                "street": z.string(),
                "city": z.string(),
                "zipcode": z.string()
            }),
            "tags": z.array(z.string()).max(10)
        })
        data = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "zipcode": "12345"
            },
            "tags": ["developer", "python", "zodiac"]
        }
        result = benchmark(schema.parse, data)
        assert result == data
    
    def test_nested_object_validation(self, benchmark):
        """Benchmark deeply nested object validation."""
        schema = z.object({
            "level1": z.object({
                "level2": z.object({
                    "level3": z.object({
                        "value": z.string()
                    })
                })
            })
        })
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        result = benchmark(schema.parse, data)
        assert result == data


class TestArrayPerformance:
    """Benchmark array validation performance."""
    
    def test_simple_array_validation(self, benchmark):
        """Benchmark simple array validation."""
        schema = z.array(z.string())
        data = ["hello", "world", "test"]
        result = benchmark(schema.parse, data)
        assert result == data
    
    def test_large_array_validation(self, benchmark):
        """Benchmark large array validation."""
        schema = z.array(z.string())
        data = ["item"] * 1000
        result = benchmark(schema.parse, data)
        assert len(result) == 1000
    
    def test_array_of_objects_validation(self, benchmark):
        """Benchmark array of objects validation."""
        schema = z.array(z.object({
            "id": z.number().int(),
            "name": z.string()
        }))
        data = [{"id": i, "name": f"item{i}"} for i in range(100)]
        result = benchmark(schema.parse, data)
        assert len(result) == 100


class TestSafeParsePerformance:
    """Benchmark safe_parse performance."""
    
    def test_safe_parse_success(self, benchmark):
        """Benchmark safe_parse with valid data."""
        schema = z.string()
        
        def safe_parse_test():
            result = schema.safe_parse("hello")
            return result["data"]
        
        result = benchmark(safe_parse_test)
        assert result == "hello"
    
    def test_safe_parse_failure(self, benchmark):
        """Benchmark safe_parse with invalid data."""
        schema = z.string()
        
        def safe_parse_test():
            result = schema.safe_parse(123)
            return result["success"]
        
        result = benchmark(safe_parse_test)
        assert result is False


class TestMemoryUsage:
    """Memory usage benchmarks."""
    
    def test_schema_creation_memory(self, benchmark):
        """Benchmark memory usage of schema creation."""
        def create_schema():
            return z.object({
                "name": z.string().min(1).max(100),
                "age": z.number().int().positive(),
                "tags": z.array(z.string()).max(10)
            })
        
        schema = benchmark(create_schema)
        assert schema is not None
    
    def test_validation_memory(self, benchmark):
        """Benchmark memory usage during validation."""
        schema = z.object({
            "items": z.array(z.object({
                "id": z.number().int(),
                "data": z.string()
            }))
        })
        
        data = {
            "items": [
                {"id": i, "data": f"data_{i}"}
                for i in range(100)
            ]
        }
        
        result = benchmark(schema.parse, data)
        assert len(result["items"]) == 100
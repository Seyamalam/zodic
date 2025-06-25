#!/usr/bin/env python3
"""
Comprehensive Collections Validation Examples for Zodic v0.2.0

This file demonstrates all collection validation features including:
- Object validation with nested structures
- Array validation with various constraints
- Optional and required fields
- Unknown key handling (strict, passthrough, strip)
- Complex nested validations
- Real-world data structures
"""

import zodic as z
from datetime import date, datetime


def basic_object_validation():
    """Demonstrate basic object validation."""
    print("=== Basic Object Validation ===")
    
    # Simple object
    user_schema = z.object({
        "name": z.string(),
        "age": z.number().int(),
        "active": z.boolean()
    })
    
    user_data = {
        "name": "John Doe",
        "age": 30,
        "active": True
    }
    
    result = user_schema.parse(user_data)
    print(f"User: {result}")
    
    # Object with optional fields
    profile_schema = z.object({
        "username": z.string(),
        "email": z.string().email().optional(),
        "bio": z.string().optional(),
        "verified": z.boolean().default(False)
    })
    
    profile_data = {
        "username": "johndoe",
        "email": "john@example.com"
    }
    
    result = profile_schema.parse(profile_data)
    print(f"Profile: {result}")
    
    print()


def nested_object_validation():
    """Demonstrate nested object validation."""
    print("=== Nested Object Validation ===")
    
    # Address object
    address_schema = z.object({
        "street": z.string(),
        "city": z.string(),
        "state": z.string().length(2),
        "zip": z.string().regex(r'^\d{5}(-\d{4})?$'),
        "country": z.string().default("US")
    })
    
    # User with nested address
    user_schema = z.object({
        "name": z.string(),
        "email": z.string().email(),
        "address": address_schema,
        "billing_address": address_schema.optional()
    })
    
    user_data = {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        }
    }
    
    result = user_schema.parse(user_data)
    print(f"User with address: {result}")
    
    print()


def object_key_handling():
    """Demonstrate different object key handling modes."""
    print("=== Object Key Handling ===")
    
    base_schema = z.object({
        "name": z.string(),
        "age": z.number().int()
    })
    
    test_data = {
        "name": "John",
        "age": 30,
        "extra": "unknown field",
        "another": "extra data"
    }
    
    # Strip mode (default) - removes unknown keys
    strip_schema = base_schema.strip()
    result = strip_schema.parse(test_data)
    print(f"Strip mode: {result}")
    
    # Passthrough mode - includes unknown keys
    passthrough_schema = base_schema.passthrough()
    result = passthrough_schema.parse(test_data)
    print(f"Passthrough mode: {result}")
    
    # Strict mode - rejects unknown keys
    strict_schema = base_schema.strict()
    try:
        result = strict_schema.parse(test_data)
    except z.ZodError as e:
        print(f"Strict mode error: {e}")
    
    # Strict mode with valid data
    valid_data = {"name": "John", "age": 30}
    result = strict_schema.parse(valid_data)
    print(f"Strict mode (valid): {result}")
    
    print()


def basic_array_validation():
    """Demonstrate basic array validation."""
    print("=== Basic Array Validation ===")
    
    # Array of strings
    tags_schema = z.array(z.string())
    tags = ["python", "validation", "zod"]
    result = tags_schema.parse(tags)
    print(f"String array: {result}")
    
    # Array of numbers
    scores_schema = z.array(z.number().int().min(0).max(100))
    scores = [85, 92, 78, 96]
    result = scores_schema.parse(scores)
    print(f"Score array: {result}")
    
    # Array with length constraints
    limited_array = z.array(z.string()).min(1).max(5)
    items = ["item1", "item2", "item3"]
    result = limited_array.parse(items)
    print(f"Limited array: {result}")
    
    # Non-empty array
    nonempty_array = z.array(z.number()).nonempty()
    numbers = [1, 2, 3]
    result = nonempty_array.parse(numbers)
    print(f"Non-empty array: {result}")
    
    print()


def array_of_objects():
    """Demonstrate arrays of objects."""
    print("=== Array of Objects ===")
    
    # Product schema
    product_schema = z.object({
        "id": z.number().int().positive(),
        "name": z.string().min(1),
        "price": z.number().positive(),
        "category": z.enum(["electronics", "clothing", "books", "home"]),
        "in_stock": z.boolean().default(True)
    })
    
    # Array of products
    products_schema = z.array(product_schema)
    
    products_data = [
        {
            "id": 1,
            "name": "Laptop",
            "price": 999.99,
            "category": "electronics"
        },
        {
            "id": 2,
            "name": "T-Shirt",
            "price": 19.99,
            "category": "clothing",
            "in_stock": False
        }
    ]
    
    result = products_schema.parse(products_data)
    print(f"Products: {result}")
    
    # User with orders
    order_schema = z.object({
        "order_id": z.string(),
        "date": z.date(),
        "total": z.number().positive(),
        "items": z.array(product_schema).min(1)
    })
    
    order_data = {
        "order_id": "ORD-001",
        "date": "2024-12-19",
        "total": 1019.98,
        "items": products_data
    }
    
    result = order_schema.parse(order_data)
    print(f"Order: {result}")
    
    print()


def complex_nested_structures():
    """Demonstrate complex nested data structures."""
    print("=== Complex Nested Structures ===")
    
    # Company organization structure
    employee_schema = z.object({
        "id": z.number().int().positive(),
        "name": z.string(),
        "email": z.string().email(),
        "role": z.enum(["developer", "manager", "designer", "analyst"]),
        "salary": z.number().positive().optional(),
        "start_date": z.date()
    })
    
    department_schema = z.object({
        "name": z.string(),
        "budget": z.number().positive(),
        "manager": employee_schema,
        "employees": z.array(employee_schema),
        "projects": z.array(z.object({
            "name": z.string(),
            "status": z.enum(["planning", "active", "completed", "cancelled"]),
            "deadline": z.date(),
            "team_members": z.array(z.number().int().positive())  # Employee IDs
        }))
    })
    
    company_schema = z.object({
        "name": z.string(),
        "founded": z.date(),
        "headquarters": z.object({
            "address": z.string(),
            "city": z.string(),
            "country": z.string()
        }),
        "departments": z.array(department_schema)
    })
    
    company_data = {
        "name": "Tech Corp",
        "founded": "2010-01-15",
        "headquarters": {
            "address": "123 Tech Street",
            "city": "San Francisco",
            "country": "USA"
        },
        "departments": [
            {
                "name": "Engineering",
                "budget": 1000000,
                "manager": {
                    "id": 1,
                    "name": "Alice Johnson",
                    "email": "alice@techcorp.com",
                    "role": "manager",
                    "start_date": "2015-03-01"
                },
                "employees": [
                    {
                        "id": 2,
                        "name": "Bob Smith",
                        "email": "bob@techcorp.com",
                        "role": "developer",
                        "start_date": "2018-06-15"
                    }
                ],
                "projects": [
                    {
                        "name": "New Platform",
                        "status": "active",
                        "deadline": "2025-06-30",
                        "team_members": [1, 2]
                    }
                ]
            }
        ]
    }
    
    result = company_schema.parse(company_data)
    print(f"Company structure validated successfully!")
    print(f"Company: {result['name']}")
    print(f"Departments: {len(result['departments'])}")
    
    print()


def api_request_response_validation():
    """Demonstrate API request/response validation."""
    print("=== API Request/Response Validation ===")
    
    # User registration request
    register_request_schema = z.object({
        "username": z.string().min(3).max(20).regex(r'^[a-zA-Z0-9_]+$'),
        "email": z.string().email(),
        "password": z.string().min(8).regex(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)'),
        "first_name": z.string().min(1),
        "last_name": z.string().min(1),
        "birth_date": z.date(),
        "terms_accepted": z.literal(True),
        "marketing_emails": z.boolean().default(False)
    })
    
    register_request = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "SecurePass123",
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": "1990-05-15",
        "terms_accepted": True
    }
    
    validated_request = register_request_schema.parse(register_request)
    print(f"Registration request validated: {validated_request['username']}")
    
    # API response schema
    api_response_schema = z.object({
        "success": z.boolean(),
        "data": z.object({
            "user_id": z.number().int().positive(),
            "username": z.string(),
            "email": z.string().email(),
            "created_at": z.datetime(),
            "profile": z.object({
                "first_name": z.string(),
                "last_name": z.string(),
                "avatar_url": z.string().url().optional()
            })
        }).optional(),
        "error": z.object({
            "code": z.string(),
            "message": z.string(),
            "details": z.array(z.string()).optional()
        }).optional(),
        "metadata": z.object({
            "request_id": z.string(),
            "timestamp": z.datetime(),
            "version": z.string()
        })
    })
    
    success_response = {
        "success": True,
        "data": {
            "user_id": 12345,
            "username": "john_doe",
            "email": "john@example.com",
            "created_at": "2024-12-19T10:30:00",
            "profile": {
                "first_name": "John",
                "last_name": "Doe"
            }
        },
        "metadata": {
            "request_id": "req_123456",
            "timestamp": "2024-12-19T10:30:00",
            "version": "v1.0"
        }
    }
    
    validated_response = api_response_schema.parse(success_response)
    print(f"API response validated: User {validated_response['data']['user_id']} created")
    
    print()


def configuration_validation():
    """Demonstrate configuration file validation."""
    print("=== Configuration Validation ===")
    
    # Database configuration
    db_config_schema = z.object({
        "host": z.string(),
        "port": z.number().int().min(1).max(65535),
        "database": z.string(),
        "username": z.string(),
        "password": z.string(),
        "ssl": z.boolean().default(True),
        "pool_size": z.number().int().min(1).max(100).default(10),
        "timeout": z.number().positive().default(30)
    })
    
    # Application configuration
    app_config_schema = z.object({
        "app_name": z.string(),
        "version": z.string().regex(r'^\d+\.\d+\.\d+$'),
        "environment": z.enum(["development", "staging", "production"]),
        "debug": z.boolean().default(False),
        "database": db_config_schema,
        "redis": z.object({
            "host": z.string(),
            "port": z.number().int().default(6379),
            "password": z.string().optional()
        }),
        "logging": z.object({
            "level": z.enum(["DEBUG", "INFO", "WARNING", "ERROR"]),
            "file": z.string().optional(),
            "max_size": z.number().int().positive().default(10485760)  # 10MB
        }),
        "features": z.object({
            "user_registration": z.boolean().default(True),
            "email_verification": z.boolean().default(True),
            "two_factor_auth": z.boolean().default(False),
            "rate_limiting": z.object({
                "enabled": z.boolean().default(True),
                "requests_per_minute": z.number().int().positive().default(60)
            })
        })
    })
    
    config_data = {
        "app_name": "MyApp",
        "version": "1.2.3",
        "environment": "production",
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "database": "myapp_prod",
            "username": "app_user",
            "password": "secure_password"
        },
        "redis": {
            "host": "redis.example.com"
        },
        "logging": {
            "level": "INFO",
            "file": "/var/log/myapp.log"
        },
        "features": {
            "two_factor_auth": True,
            "rate_limiting": {
                "requests_per_minute": 100
            }
        }
    }
    
    validated_config = app_config_schema.parse(config_data)
    print(f"Configuration validated: {validated_config['app_name']} v{validated_config['version']}")
    print(f"Environment: {validated_config['environment']}")
    print(f"Database: {validated_config['database']['host']}:{validated_config['database']['port']}")
    
    print()


def data_transformation_examples():
    """Demonstrate data transformations in collections."""
    print("=== Data Transformations ===")
    
    # Transform user data
    user_transform_schema = z.object({
        "first_name": z.string().transform(str.title),
        "last_name": z.string().transform(str.title),
        "email": z.string().email().transform(str.lower),
        "tags": z.array(z.string().transform(str.lower)),
        "metadata": z.object({
            "created_at": z.datetime(),
            "updated_at": z.datetime()
        }).transform(lambda obj: {
            **obj,
            "last_modified": obj["updated_at"]
        })
    })
    
    user_data = {
        "first_name": "john",
        "last_name": "DOE",
        "email": "John.Doe@EXAMPLE.COM",
        "tags": ["PYTHON", "Developer", "BACKEND"],
        "metadata": {
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-12-19T10:30:00"
        }
    }
    
    result = user_transform_schema.parse(user_data)
    print(f"Transformed user: {result}")
    
    # Transform array data
    scores_transform = z.array(z.number()).transform(
        lambda scores: {
            "scores": scores,
            "average": sum(scores) / len(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "min": min(scores) if scores else 0
        }
    )
    
    scores = [85, 92, 78, 96, 88]
    result = scores_transform.parse(scores)
    print(f"Score analysis: {result}")
    
    print()


def error_handling_examples():
    """Demonstrate error handling in collections."""
    print("=== Error Handling Examples ===")
    
    # Complex schema for error testing
    complex_schema = z.object({
        "user": z.object({
            "name": z.string().min(2),
            "email": z.string().email(),
            "age": z.number().int().positive(),
            "preferences": z.object({
                "theme": z.enum(["light", "dark"]),
                "notifications": z.boolean()
            })
        }),
        "items": z.array(z.object({
            "id": z.number().int().positive(),
            "name": z.string().min(1),
            "price": z.number().positive()
        })).min(1)
    })
    
    # Invalid data with multiple errors
    invalid_data = {
        "user": {
            "name": "A",  # Too short
            "email": "invalid-email",  # Invalid format
            "age": -5,  # Not positive
            "preferences": {
                "theme": "blue",  # Invalid enum
                "notifications": "yes"  # Wrong type
            }
        },
        "items": [
            {
                "id": -1,  # Not positive
                "name": "",  # Too short
                "price": -10  # Not positive
            }
        ]
    }
    
    result = complex_schema.safe_parse(invalid_data)
    if not result["success"]:
        print("Validation errors found:")
        errors = result["error"].flatten()
        for path, messages in errors.items():
            print(f"  {path}: {', '.join(messages)}")
    
    print()


def main():
    """Run all collections validation examples."""
    print("Zodic Collections Validation Examples")
    print("=" * 50)
    
    basic_object_validation()
    nested_object_validation()
    object_key_handling()
    basic_array_validation()
    array_of_objects()
    complex_nested_structures()
    api_request_response_validation()
    configuration_validation()
    data_transformation_examples()
    error_handling_examples()
    
    print("=" * 50)
    print("All collections validation examples completed!")


if __name__ == "__main__":
    main()
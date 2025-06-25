#!/usr/bin/env python3
"""
Basic Zodic usage examples.

This file demonstrates the core features of Zodic with practical examples.
Updated for v0.2.0 with comprehensive feature coverage.
"""

import zodic as z
from datetime import date, datetime

def basic_types_example():
    """Demonstrate basic type validation."""
    print("=== Basic Types ===")
    
    # String validation
    name_schema = z.string().min(1).max(50)
    name = name_schema.parse("Alice")
    print(f"Name: {name}")
    
    # Email validation
    email_schema = z.string().email()
    email = email_schema.parse("alice@example.com")
    print(f"Email: {email}")
    
    # Number validation
    age_schema = z.number().int().min(0).max(120)
    age = age_schema.parse(30)
    print(f"Age: {age}")
    
    # Boolean validation
    active_schema = z.boolean()
    is_active = active_schema.parse(True)
    print(f"Active: {is_active}")
    
    # Enum validation
    role_schema = z.enum(["admin", "user", "guest"])
    role = role_schema.parse("admin")
    print(f"Role: {role}")
    
    # Literal validation
    status_schema = z.literal("active")
    status = status_schema.parse("active")
    print(f"Status: {status}")


def object_validation_example():
    """Demonstrate object validation."""
    print("\n=== Object Validation ===")
    
    user_schema = z.object({
        "name": z.string().min(1),
        "email": z.string().refine(lambda x: "@" in x, "Invalid email"),
        "age": z.number().int().min(18),
        "is_premium": z.boolean().default(False),
        "tags": z.array(z.string()).optional()
    })
    
    user_data = {
        "name": "John Doe",
        "email": "john@example.com", 
        "age": 25,
        "tags": ["developer", "python"]
    }
    
    user = user_schema.parse(user_data)
    print(f"User: {user}")


def array_validation_example():
    """Demonstrate array validation."""
    print("\n=== Array Validation ===")
    
    # Array of strings
    tags_schema = z.array(z.string().min(1)).min(1).max(5)
    tags = tags_schema.parse(["python", "validation", "zod"])
    print(f"Tags: {tags}")
    
    # Array of objects
    users_schema = z.array(z.object({
        "name": z.string(),
        "score": z.number().min(0).max(100)
    }))
    
    users_data = [
        {"name": "Alice", "score": 95},
        {"name": "Bob", "score": 87}
    ]
    
    users = users_schema.parse(users_data)
    print(f"Users: {users}")


def transformations_example():
    """Demonstrate data transformations."""
    print("\n=== Transformations ===")
    
    # String transformation
    clean_string = z.string().transform(str.strip).transform(str.upper)
    result = clean_string.parse("  hello world  ")
    print(f"Cleaned string: '{result}'")
    
    # Number transformation
    doubled = z.number().transform(lambda x: x * 2)
    result = doubled.parse(21)
    print(f"Doubled: {result}")


def error_handling_example():
    """Demonstrate error handling."""
    print("\n=== Error Handling ===")
    
    schema = z.object({
        "user": z.object({
            "name": z.string().min(2),
            "age": z.number().int().positive()
        })
    })
    
    # Valid data
    try:
        valid_data = {"user": {"name": "Alice", "age": 30}}
        result = schema.parse(valid_data)
        print(f"Valid: {result}")
    except z.ZodError as e:
        print(f"Error: {e}")
    
    # Invalid data
    try:
        invalid_data = {"user": {"name": "A", "age": "thirty"}}
        result = schema.parse(invalid_data)
    except z.ZodError as e:
        print(f"Validation error: {e}")
    
    # Safe parse
    result = schema.safe_parse(invalid_data)
    if result["success"]:
        print(f"Success: {result['data']}")
    else:
        print(f"Failed safely: {result['error']}")


def api_validation_example():
    """Demonstrate API request validation."""
    print("\n=== API Validation ===")
    
    # Define API schema
    create_post_schema = z.object({
        "title": z.string().min(1).max(200),
        "content": z.string().min(10),
        "author": z.object({
            "name": z.string().min(1),
            "email": z.string().refine(lambda x: "@" in x, "Invalid email")
        }),
        "tags": z.array(z.string()).max(10).default([]),
        "published": z.boolean().default(False),
        "metadata": z.object({
            "priority": z.number().int().min(1).max(5).default(3),
            "category": z.string().optional()
        }).optional()
    })
    
    # Sample API request
    api_request = {
        "title": "Getting Started with Zodic",
        "content": "Zodic is a powerful validation library for Python...",
        "author": {
            "name": "Zodic Team",
            "email": "team@zodic.dev"
        },
        "tags": ["python", "validation"],
        "metadata": {
            "priority": 4,
            "category": "tutorial"
        }
    }
    
    try:
        validated = create_post_schema.parse(api_request)
        print("API request validated successfully!")
        print(f"Title: {validated['title']}")
        print(f"Author: {validated['author']['name']}")
        print(f"Published: {validated['published']}")
    except z.ZodError as e:
        print(f"API validation failed: {e}")


def new_features_example():
    """Demonstrate new features in v0.2.0."""
    print("\n=== New Features (v0.2.0) ===")
    
    # Date validation
    from datetime import date, datetime
    date_schema = z.date()
    parsed_date = date_schema.parse("2024-12-19")
    print(f"Parsed date: {parsed_date}")
    
    # DateTime validation
    datetime_schema = z.datetime()
    parsed_datetime = datetime_schema.parse("2024-12-19T10:30:00")
    print(f"Parsed datetime: {parsed_datetime}")
    
    # URL validation
    url_schema = z.string().url()
    url = url_schema.parse("https://example.com")
    print(f"Valid URL: {url}")
    
    # Regex validation
    code_schema = z.string().regex(r"^[A-Z]{2,3}$")
    code = code_schema.parse("ABC")
    print(f"Valid code: {code}")
    
    # Union operator
    flexible_schema = z.string() | z.number()
    result1 = flexible_schema.parse("hello")
    result2 = flexible_schema.parse(42)
    print(f"Union results: {result1}, {result2}")
    
    # Fixed positive validation
    positive_schema = z.number().positive()
    positive_num = positive_schema.parse(5)
    print(f"Positive number: {positive_num}")
    
    try:
        positive_schema.parse(0)  # This should fail now
    except z.ZodError as e:
        print(f"Zero correctly rejected: {e}")


def main():
    """Run all examples."""
    print("Zodic Examples")
    print("=" * 50)
    
    basic_types_example()
    object_validation_example()
    array_validation_example()
    transformations_example()
    error_handling_example()
    api_validation_example()
    new_features_example()
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
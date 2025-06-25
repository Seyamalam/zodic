#!/usr/bin/env python3
"""
Advanced Zodic Features Examples for v0.2.0

This file demonstrates advanced features including:
- Literal and enum validation
- Union types and operator
- Optional, nullable, and default values
- Transformations and refinements
- Custom validators
- Error handling and formatting
- Performance considerations
"""

import zodic as z
from datetime import date, datetime
from typing import Any, Dict, List


def literal_validation_examples():
    """Demonstrate literal value validation."""
    print("=== Literal Validation ===")
    
    # Basic literal values
    status_schema = z.literal("active")
    print(f"Status: {status_schema.parse('active')}")
    
    # Number literal
    version_schema = z.literal(1)
    print(f"Version: {version_schema.parse(1)}")
    
    # Boolean literal
    admin_schema = z.literal(True)
    print(f"Admin flag: {admin_schema.parse(True)}")
    
    # Multiple literals in object
    api_response = z.object({
        "status": z.literal("success"),
        "version": z.literal("v1"),
        "code": z.literal(200)
    })
    
    response_data = {
        "status": "success",
        "version": "v1",
        "code": 200
    }
    
    result = api_response.parse(response_data)
    print(f"API response: {result}")
    
    # Error cases
    print("\nLiteral validation errors:")
    try:
        status_schema.parse("inactive")
    except z.ZodError as e:
        print(f"❌ Wrong literal: {e}")
    
    print()


def enum_validation_examples():
    """Demonstrate enum validation."""
    print("=== Enum Validation ===")
    
    # Basic enum
    color_schema = z.enum(["red", "green", "blue"])
    print(f"Color: {color_schema.parse('red')}")
    
    # Status enum
    order_status = z.enum(["pending", "processing", "shipped", "delivered", "cancelled"])
    print(f"Order status: {order_status.parse('shipped')}")
    
    # Number enum
    priority_schema = z.enum([1, 2, 3, 4, 5])
    print(f"Priority: {priority_schema.parse(3)}")
    
    # Mixed type enum
    mixed_enum = z.enum(["auto", 0, True])
    print(f"Mixed enum (string): {mixed_enum.parse('auto')}")
    print(f"Mixed enum (number): {mixed_enum.parse(0)}")
    print(f"Mixed enum (boolean): {mixed_enum.parse(True)}")
    
    # Enum in object
    user_role = z.object({
        "username": z.string(),
        "role": z.enum(["admin", "moderator", "user"]),
        "permissions": z.array(z.enum(["read", "write", "delete"]))
    })
    
    user_data = {
        "username": "john_doe",
        "role": "admin",
        "permissions": ["read", "write", "delete"]
    }
    
    result = user_role.parse(user_data)
    print(f"User with role: {result}")
    
    # Error cases
    print("\nEnum validation errors:")
    try:
        color_schema.parse("purple")
    except z.ZodError as e:
        print(f"❌ Invalid enum value: {e}")
    
    print()


def union_validation_examples():
    """Demonstrate union type validation."""
    print("=== Union Validation ===")
    
    # Basic union with function
    string_or_number = z.union([z.string(), z.number()])
    print(f"String: {string_or_number.parse('hello')}")
    print(f"Number: {string_or_number.parse(42)}")
    
    # Union with operator (new in v0.2.0)
    text_or_num = z.string() | z.number()
    print(f"Union operator string: {text_or_num.parse('world')}")
    print(f"Union operator number: {text_or_num.parse(3.14)}")
    
    # Complex union
    id_schema = z.string().regex(r'^[A-Z]{2}\d{6}$') | z.number().int().positive()
    print(f"String ID: {id_schema.parse('AB123456')}")
    print(f"Number ID: {id_schema.parse(789)}")
    
    # Union with different validations
    flexible_input = (z.string().email() | 
                     z.string().regex(r'^\+\d{10,15}$') |  # Phone
                     z.number().int().positive())  # User ID
    
    print(f"Email input: {flexible_input.parse('user@example.com')}")
    print(f"Phone input: {flexible_input.parse('+1234567890')}")
    print(f"ID input: {flexible_input.parse(12345)}")
    
    # Union in object
    contact_schema = z.object({
        "name": z.string(),
        "contact": z.string().email() | z.string().regex(r'^\+\d{10,15}$'),
        "id": z.string() | z.number().int()
    })
    
    contact_data = {
        "name": "Jane Doe",
        "contact": "jane@example.com",
        "id": "USER_001"
    }
    
    result = contact_schema.parse(contact_data)
    print(f"Contact: {result}")
    
    # Error cases
    print("\nUnion validation errors:")
    try:
        string_or_number.parse(True)  # Boolean not in union
    except z.ZodError as e:
        print(f"❌ No union match: {e}")
    
    print()


def optional_nullable_default_examples():
    """Demonstrate optional, nullable, and default values."""
    print("=== Optional, Nullable, and Default Values ===")
    
    # Optional fields
    user_schema = z.object({
        "name": z.string(),
        "email": z.string().email().optional(),
        "phone": z.string().optional(),
        "bio": z.string().optional()
    })
    
    # With optional fields
    user_with_email = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    result = user_schema.parse(user_with_email)
    print(f"User with email: {result}")
    
    # Without optional fields
    user_minimal = {"name": "Jane Doe"}
    result = user_schema.parse(user_minimal)
    print(f"Minimal user: {result}")
    
    # Nullable fields
    nullable_schema = z.object({
        "title": z.string(),
        "description": z.string().nullable(),
        "tags": z.array(z.string()).nullable()
    })
    
    data_with_nulls = {
        "title": "Test Article",
        "description": None,
        "tags": None
    }
    result = nullable_schema.parse(data_with_nulls)
    print(f"Data with nulls: {result}")
    
    # Default values
    config_schema = z.object({
        "host": z.string(),
        "port": z.number().int().default(8080),
        "debug": z.boolean().default(False),
        "timeout": z.number().default(30),
        "retries": z.number().int().default(3)
    })
    
    minimal_config = {"host": "localhost"}
    result = config_schema.parse(minimal_config)
    print(f"Config with defaults: {result}")
    
    # Chaining optional, nullable, and default
    flexible_field = z.string().optional().nullable().default("default_value")
    
    from zodic.core.base import UNDEFINED
    print(f"Undefined -> default: {flexible_field.safe_parse(UNDEFINED)['data']}")
    print(f"None -> None: {flexible_field.safe_parse(None)['data']}")
    print(f"Value -> value: {flexible_field.safe_parse('actual')['data']}")
    
    print()


def transformation_examples():
    """Demonstrate data transformations."""
    print("=== Data Transformations ===")
    
    # String transformations
    name_schema = z.string().transform(str.title)
    print(f"Title case: {name_schema.parse('john doe')}")
    
    # Number transformations
    percentage_schema = z.number().min(0).max(1).transform(lambda x: f"{x*100:.1f}%")
    print(f"Percentage: {percentage_schema.parse(0.856)}")
    
    # Chained transformations
    clean_email = (z.string()
                  .transform(str.strip)
                  .transform(str.lower)
                  .email())
    print(f"Clean email: {clean_email.parse('  John.Doe@EXAMPLE.COM  ')}")
    
    # Object transformations
    user_transform = z.object({
        "first_name": z.string(),
        "last_name": z.string(),
        "birth_date": z.date()
    }).transform(lambda user: {
        **user,
        "full_name": f"{user['first_name']} {user['last_name']}",
        "age": (date.today() - user["birth_date"]).days // 365
    })
    
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": "1990-05-15"
    }
    
    result = user_transform.parse(user_data)
    print(f"Transformed user: {result}")
    
    # Array transformations
    stats_transform = z.array(z.number()).transform(lambda nums: {
        "values": nums,
        "count": len(nums),
        "sum": sum(nums),
        "average": sum(nums) / len(nums) if nums else 0,
        "min": min(nums) if nums else 0,
        "max": max(nums) if nums else 0
    })
    
    numbers = [10, 20, 30, 40, 50]
    result = stats_transform.parse(numbers)
    print(f"Number stats: {result}")
    
    # Complex transformation pipeline
    product_pipeline = z.object({
        "name": z.string().transform(str.title),
        "price": z.number().positive(),
        "category": z.string().transform(str.lower),
        "tags": z.array(z.string().transform(str.lower))
    }).transform(lambda product: {
        **product,
        "slug": product["name"].lower().replace(" ", "-"),
        "price_formatted": f"${product['price']:.2f}",
        "search_terms": [product["name"].lower()] + product["tags"]
    })
    
    product_data = {
        "name": "wireless headphones",
        "price": 99.99,
        "category": "ELECTRONICS",
        "tags": ["AUDIO", "Wireless", "BLUETOOTH"]
    }
    
    result = product_pipeline.parse(product_data)
    print(f"Product pipeline: {result}")
    
    print()


def refinement_examples():
    """Demonstrate custom refinements."""
    print("=== Custom Refinements ===")
    
    # Simple refinement
    even_number = z.number().int().refine(
        lambda x: x % 2 == 0,
        "Number must be even"
    )
    print(f"Even number: {even_number.parse(42)}")
    
    # Multiple refinements
    strong_password = (z.string()
                      .min(8)
                      .refine(lambda x: any(c.isupper() for c in x), "Must contain uppercase")
                      .refine(lambda x: any(c.islower() for c in x), "Must contain lowercase")
                      .refine(lambda x: any(c.isdigit() for c in x), "Must contain digit")
                      .refine(lambda x: any(c in "!@#$%^&*" for c in x), "Must contain special char"))
    
    print(f"Strong password: {strong_password.parse('MySecure123!')}")
    
    # Business logic refinements
    def is_business_day(d):
        return d.weekday() < 5
    
    business_date = z.date().refine(is_business_day, "Must be a business day")
    monday = date(2024, 12, 16)  # A Monday
    print(f"Business date: {business_date.parse(monday)}")
    
    # Complex object refinement
    def validate_age_consistency(person):
        birth_year = person["birth_date"].year
        current_year = date.today().year
        calculated_age = current_year - birth_year
        return abs(calculated_age - person["age"]) <= 1
    
    person_schema = z.object({
        "name": z.string(),
        "age": z.number().int().min(0).max(150),
        "birth_date": z.date()
    }).refine(validate_age_consistency, "Age and birth date don't match")
    
    person_data = {
        "name": "John Doe",
        "age": 34,
        "birth_date": "1990-05-15"
    }
    
    result = person_schema.parse(person_data)
    print(f"Person with age validation: {result}")
    
    # Array refinement
    unique_array = z.array(z.string()).refine(
        lambda arr: len(arr) == len(set(arr)),
        "Array must contain unique values"
    )
    
    unique_tags = ["python", "javascript", "typescript"]
    print(f"Unique array: {unique_array.parse(unique_tags)}")
    
    print()


def custom_validator_examples():
    """Demonstrate custom validator patterns."""
    print("=== Custom Validator Patterns ===")
    
    # Credit card validator
    def luhn_algorithm(card_number):
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        return luhn_checksum(card_number) == 0
    
    credit_card = (z.string()
                  .regex(r'^\d{16}$')
                  .transform(int)
                  .refine(luhn_algorithm, "Invalid credit card number"))
    
    # Test credit card number (this is a valid test number)
    test_card = "4532015112830366"
    print(f"Valid credit card: {credit_card.parse(test_card)}")
    
    # ISBN validator
    def validate_isbn13(isbn):
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        
        checksum = 0
        for i, digit in enumerate(isbn[:-1]):
            weight = 1 if i % 2 == 0 else 3
            checksum += int(digit) * weight
        
        check_digit = (10 - (checksum % 10)) % 10
        return check_digit == int(isbn[-1])
    
    isbn_schema = z.string().refine(validate_isbn13, "Invalid ISBN-13")
    
    # Test ISBN (valid test number)
    test_isbn = "9780134685991"
    print(f"Valid ISBN: {isbn_schema.parse(test_isbn)}")
    
    # Custom email domain validator
    def validate_company_email(email):
        allowed_domains = ["company.com", "subsidiary.com", "partner.org"]
        domain = email.split("@")[1] if "@" in email else ""
        return domain in allowed_domains
    
    company_email = (z.string()
                     .email()
                     .refine(validate_company_email, "Must use company email domain"))
    
    print(f"Company email: {company_email.parse('user@company.com')}")
    
    # Geographic coordinate validator
    def validate_coordinates(coords):
        lat, lon = coords["latitude"], coords["longitude"]
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    coordinates_schema = z.object({
        "latitude": z.number(),
        "longitude": z.number()
    }).refine(validate_coordinates, "Invalid geographic coordinates")
    
    coords_data = {"latitude": 40.7128, "longitude": -74.0060}  # NYC
    print(f"Valid coordinates: {coordinates_schema.parse(coords_data)}")
    
    print()


def error_handling_and_formatting():
    """Demonstrate advanced error handling."""
    print("=== Advanced Error Handling ===")
    
    # Complex schema for error demonstration
    complex_schema = z.object({
        "user": z.object({
            "name": z.string().min(2).max(50),
            "email": z.string().email(),
            "age": z.number().int().min(18).max(120),
            "role": z.enum(["admin", "user", "moderator"])
        }),
        "preferences": z.object({
            "theme": z.enum(["light", "dark"]),
            "notifications": z.boolean(),
            "language": z.string().regex(r'^[a-z]{2}$')
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
            "age": 15,  # Too young
            "role": "guest"  # Invalid enum
        },
        "preferences": {
            "theme": "blue",  # Invalid enum
            "notifications": "yes",  # Wrong type
            "language": "english"  # Wrong format
        },
        "items": []  # Empty array
    }
    
    # Safe parse to get detailed errors
    result = complex_schema.safe_parse(invalid_data)
    
    if not result["success"]:
        error = result["error"]
        
        # Basic error message
        print(f"Basic error: {error}")
        print()
        
        # Flattened errors
        print("Flattened errors:")
        flattened = error.flatten()
        for path, messages in flattened.items():
            print(f"  {path}: {', '.join(messages)}")
        print()
        
        # Formatted errors
        print("Formatted errors:")
        formatted = error.format()
        for err in formatted:
            print(f"  Path: {'.'.join(map(str, err['path']))}")
            print(f"  Code: {err['code']}")
            print(f"  Message: {err['message']}")
            print(f"  Received: {err['received']}")
            if err['expected']:
                print(f"  Expected: {err['expected']}")
            print()
    
    # Custom error handling function
    def handle_validation_error(error: z.ZodError) -> Dict[str, Any]:
        """Convert ZodError to API-friendly format."""
        return {
            "error": "validation_failed",
            "message": "The provided data is invalid",
            "details": [
                {
                    "field": ".".join(map(str, issue["path"])) or "root",
                    "code": issue["code"],
                    "message": issue["message"],
                    "received": str(issue["received"])
                }
                for issue in error.issues
            ]
        }
    
    api_error = handle_validation_error(result["error"])
    print("API-friendly error format:")
    print(f"Error: {api_error['error']}")
    print(f"Message: {api_error['message']}")
    print("Details:")
    for detail in api_error["details"]:
        print(f"  - {detail['field']}: {detail['message']}")
    
    print()


def performance_considerations():
    """Demonstrate performance considerations."""
    print("=== Performance Considerations ===")
    
    # Schema reuse (good practice)
    user_schema = z.object({
        "name": z.string(),
        "email": z.string().email(),
        "age": z.number().int()
    })
    
    # Reuse the same schema instance
    users_data = [
        {"name": "John", "email": "john@example.com", "age": 30},
        {"name": "Jane", "email": "jane@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 35}
    ]
    
    validated_users = [user_schema.parse(user) for user in users_data]
    print(f"Validated {len(validated_users)} users efficiently")
    
    # Safe parse for bulk operations
    results = [user_schema.safe_parse(user) for user in users_data]
    successful = [r["data"] for r in results if r["success"]]
    failed = [r["error"] for r in results if not r["success"]]
    
    print(f"Bulk validation: {len(successful)} successful, {len(failed)} failed")
    
    # Avoid creating schemas in loops (bad practice)
    # Instead of: [z.string().email().parse(email) for email in emails]
    # Do this:
    email_schema = z.string().email()
    emails = ["user1@example.com", "user2@example.com", "user3@example.com"]
    validated_emails = [email_schema.parse(email) for email in emails]
    print(f"Validated {len(validated_emails)} emails efficiently")
    
    print()


def main():
    """Run all advanced feature examples."""
    print("Zodic Advanced Features Examples")
    print("=" * 50)
    
    literal_validation_examples()
    enum_validation_examples()
    union_validation_examples()
    optional_nullable_default_examples()
    transformation_examples()
    refinement_examples()
    custom_validator_examples()
    error_handling_and_formatting()
    performance_considerations()
    
    print("=" * 50)
    print("All advanced feature examples completed!")


if __name__ == "__main__":
    main()
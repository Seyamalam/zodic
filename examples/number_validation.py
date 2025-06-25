#!/usr/bin/env python3
"""
Comprehensive Number Validation Examples for Zodic v0.2.0

This file demonstrates all number validation features including:
- Basic number validation
- Integer constraints
- Range validation (min/max)
- Positive/negative/nonnegative validation
- Transformations
- Custom refinements
- Edge cases and precision
"""

import zodic as z
import math


def basic_number_validation():
    """Demonstrate basic number validation."""
    print("=== Basic Number Validation ===")
    
    # Simple number (int or float)
    number_schema = z.number()
    print(f"Integer: {number_schema.parse(42)}")
    print(f"Float: {number_schema.parse(3.14159)}")
    print(f"Negative: {number_schema.parse(-17)}")
    print(f"Zero: {number_schema.parse(0)}")
    
    # Large numbers
    print(f"Large int: {number_schema.parse(2**63 - 1)}")
    print(f"Scientific notation: {number_schema.parse(1.23e-4)}")
    
    print()


def integer_validation():
    """Demonstrate integer-only validation."""
    print("=== Integer Validation ===")
    
    # Integer only
    int_schema = z.number().int()
    print(f"Valid integer: {int_schema.parse(42)}")
    print(f"Float converted to int: {int_schema.parse(42.0)}")
    
    # Integer with range
    age_schema = z.number().int().min(0).max(150)
    print(f"Valid age: {age_schema.parse(25)}")
    
    # Test invalid cases
    print("\nInvalid integer cases:")
    try:
        int_schema.parse(3.14)
    except z.ZodError as e:
        print(f"❌ Float rejected: {e}")
    
    try:
        age_schema.parse(-5)
    except z.ZodError as e:
        print(f"❌ Negative age rejected: {e}")
    
    print()


def range_validation():
    """Demonstrate range validation."""
    print("=== Range Validation ===")
    
    # Basic range
    percentage = z.number().min(0).max(100)
    print(f"Percentage: {percentage.parse(85.5)}")
    
    # Temperature range
    celsius = z.number().min(-273.15).max(1000)
    print(f"Temperature: {celsius.parse(23.5)}°C")
    
    # Price range
    price = z.number().min(0.01).max(999999.99)
    print(f"Price: ${price.parse(29.99)}")
    
    # Test boundary values
    boundary_test = z.number().min(10).max(20)
    print(f"Min boundary: {boundary_test.parse(10)}")
    print(f"Max boundary: {boundary_test.parse(20)}")
    
    # Test invalid ranges
    print("\nInvalid range cases:")
    try:
        percentage.parse(150)
    except z.ZodError as e:
        print(f"❌ Over 100%: {e}")
    
    try:
        celsius.parse(-300)
    except z.ZodError as e:
        print(f"❌ Below absolute zero: {e}")
    
    print()


def positive_negative_validation():
    """Demonstrate positive/negative validation."""
    print("=== Positive/Negative Validation ===")
    
    # Positive numbers (> 0)
    positive_schema = z.number().positive()
    print(f"Positive: {positive_schema.parse(1)}")
    print(f"Small positive: {positive_schema.parse(0.000001)}")
    print(f"Large positive: {positive_schema.parse(1000000)}")
    
    # Negative numbers (< 0)
    negative_schema = z.number().negative()
    print(f"Negative: {negative_schema.parse(-1)}")
    print(f"Small negative: {negative_schema.parse(-0.000001)}")
    
    # Non-negative (>= 0)
    nonnegative_schema = z.number().nonnegative()
    print(f"Non-negative zero: {nonnegative_schema.parse(0)}")
    print(f"Non-negative positive: {nonnegative_schema.parse(5)}")
    
    # Test zero edge cases
    print("\nZero edge cases:")
    try:
        positive_schema.parse(0)
    except z.ZodError as e:
        print(f"✅ Positive correctly rejects zero: {e}")
    
    try:
        negative_schema.parse(0)
    except z.ZodError as e:
        print(f"✅ Negative correctly rejects zero: {e}")
    
    print(f"✅ Non-negative accepts zero: {nonnegative_schema.parse(0)}")
    
    print()


def chained_number_validation():
    """Demonstrate chaining number validations."""
    print("=== Chained Number Validations ===")
    
    # Age validation
    age = z.number().int().positive().max(150)
    print(f"Valid age: {age.parse(25)}")
    
    # Score validation
    score = z.number().int().min(0).max(100)
    print(f"Test score: {score.parse(87)}")
    
    # Currency amount
    currency = z.number().positive().max(1000000)
    print(f"Currency: ${currency.parse(1234.56)}")
    
    # Precision number
    precision = z.number().positive().min(0.01).max(99.99)
    print(f"Precision value: {precision.parse(12.34)}")
    
    # Complex validation
    complex_num = (z.number()
                  .int()
                  .positive()
                  .min(1000)
                  .max(9999))
    print(f"4-digit PIN: {complex_num.parse(1234)}")
    
    print()


def number_transformations():
    """Demonstrate number transformations."""
    print("=== Number Transformations ===")
    
    # Basic transformations
    double_schema = z.number().transform(lambda x: x * 2)
    print(f"Doubled: {double_schema.parse(21)}")
    
    square_schema = z.number().transform(lambda x: x ** 2)
    print(f"Squared: {square_schema.parse(5)}")
    
    # Rounding
    rounded_schema = z.number().transform(lambda x: round(x, 2))
    print(f"Rounded: {rounded_schema.parse(3.14159)}")
    
    # Currency formatting (as number)
    currency_cents = z.number().transform(lambda x: round(x * 100))
    print(f"Dollars to cents: {currency_cents.parse(12.34)}")
    
    # Mathematical operations
    fahrenheit_to_celsius = z.number().transform(lambda f: round((f - 32) * 5/9, 2))
    print(f"32°F to Celsius: {fahrenheit_to_celsius.parse(32)}")
    
    # Chained transformations
    normalize_percentage = (z.number()
                           .min(0)
                           .max(1)
                           .transform(lambda x: x * 100)
                           .transform(lambda x: round(x, 1)))
    print(f"Normalized percentage: {normalize_percentage.parse(0.856)}")
    
    print()


def number_refinements():
    """Demonstrate custom number refinements."""
    print("=== Number Refinements ===")
    
    # Even numbers only
    even_schema = z.number().int().refine(
        lambda x: x % 2 == 0,
        "Number must be even"
    )
    print(f"Even number: {even_schema.parse(42)}")
    
    # Prime number validation
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    prime_schema = z.number().int().positive().refine(
        is_prime,
        "Number must be prime"
    )
    print(f"Prime number: {prime_schema.parse(17)}")
    
    # Fibonacci number
    def is_fibonacci(n):
        if n < 0:
            return False
        a, b = 0, 1
        while a < n:
            a, b = b, a + b
        return a == n
    
    fibonacci_schema = z.number().int().nonnegative().refine(
        is_fibonacci,
        "Number must be in Fibonacci sequence"
    )
    print(f"Fibonacci number: {fibonacci_schema.parse(21)}")
    
    # Multiple of specific number
    multiple_of_5 = z.number().refine(
        lambda x: x % 5 == 0,
        "Number must be multiple of 5"
    )
    print(f"Multiple of 5: {multiple_of_5.parse(25)}")
    
    # Business logic refinements
    valid_quantity = z.number().int().positive().refine(
        lambda x: x <= 1000,
        "Quantity cannot exceed 1000"
    ).refine(
        lambda x: x % 10 == 0,
        "Quantity must be in multiples of 10"
    )
    print(f"Valid quantity: {valid_quantity.parse(50)}")
    
    print()


def precision_and_edge_cases():
    """Demonstrate precision handling and edge cases."""
    print("=== Precision and Edge Cases ===")
    
    # Floating point precision
    precision_schema = z.number().min(0.1).max(0.9)
    print(f"Boundary test 0.1: {precision_schema.parse(0.1)}")
    print(f"Boundary test 0.9: {precision_schema.parse(0.9)}")
    
    # Very small numbers
    tiny_schema = z.number().positive()
    print(f"Tiny positive: {tiny_schema.parse(1e-10)}")
    
    # Very large numbers
    large_schema = z.number()
    print(f"Large number: {large_schema.parse(1.7976931348623157e+308)}")
    
    # NaN and infinity handling
    print("\nSpecial float values:")
    try:
        z.number().parse(float('nan'))
    except z.ZodError as e:
        print(f"✅ NaN rejected: {e}")
    
    try:
        z.number().parse(float('inf'))
    except z.ZodError as e:
        print(f"✅ Infinity rejected: {e}")
    
    # Boolean rejection (new in v0.2.0)
    try:
        z.number().parse(True)
    except z.ZodError as e:
        print(f"✅ Boolean rejected: {e}")
    
    print()


def real_world_examples():
    """Demonstrate real-world number validation scenarios."""
    print("=== Real-World Number Examples ===")
    
    # Credit card validation (Luhn algorithm)
    def luhn_check(card_number):
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
    
    credit_card = (z.number()
                  .int()
                  .min(1000000000000000)  # 16 digits min
                  .max(9999999999999999)  # 16 digits max
                  .refine(luhn_check, "Invalid credit card number"))
    
    # Example valid credit card (test number)
    print(f"Valid credit card: {credit_card.parse(4532015112830366)}")
    
    # GPS coordinates
    latitude = z.number().min(-90).max(90)
    longitude = z.number().min(-180).max(180)
    print(f"Latitude: {latitude.parse(40.7128)}")
    print(f"Longitude: {longitude.parse(-74.0060)}")
    
    # Financial calculations
    interest_rate = z.number().min(0).max(1).transform(lambda x: x * 100)
    print(f"Interest rate: {interest_rate.parse(0.045)}%")
    
    # Inventory management
    stock_level = z.number().int().nonnegative().max(10000)
    print(f"Stock level: {stock_level.parse(150)} units")
    
    # Performance metrics
    cpu_usage = z.number().min(0).max(100).transform(lambda x: round(x, 1))
    print(f"CPU usage: {cpu_usage.parse(67.8)}%")
    
    print()


def error_handling_examples():
    """Demonstrate number validation error handling."""
    print("=== Number Validation Error Handling ===")
    
    # Complex schema for testing
    complex_schema = (z.number()
                     .int()
                     .positive()
                     .min(10)
                     .max(100)
                     .refine(lambda x: x % 5 == 0, "Must be multiple of 5"))
    
    test_cases = [
        3.14,    # Not integer
        -5,      # Not positive
        5,       # Below minimum
        150,     # Above maximum
        23,      # Not multiple of 5
        50       # Valid
    ]
    
    for test in test_cases:
        result = complex_schema.safe_parse(test)
        if result["success"]:
            print(f"✅ Valid: {result['data']}")
        else:
            print(f"❌ Invalid {test}: {result['error']}")
    
    print()


def main():
    """Run all number validation examples."""
    print("Zodic Number Validation Examples")
    print("=" * 50)
    
    basic_number_validation()
    integer_validation()
    range_validation()
    positive_negative_validation()
    chained_number_validation()
    number_transformations()
    number_refinements()
    precision_and_edge_cases()
    real_world_examples()
    error_handling_examples()
    
    print("=" * 50)
    print("All number validation examples completed!")


if __name__ == "__main__":
    main()
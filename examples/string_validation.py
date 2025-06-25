#!/usr/bin/env python3
"""
Comprehensive String Validation Examples for Zodic v0.2.0

This file demonstrates all string validation features including:
- Basic length constraints
- Email validation
- URL validation
- Regex patterns
- Chaining validations
- Custom refinements
"""

import zodic as z
import re


def basic_string_validation():
    """Demonstrate basic string validation."""
    print("=== Basic String Validation ===")
    
    # Simple string
    name_schema = z.string()
    print(f"Simple string: {name_schema.parse('Hello World')}")
    
    # Length constraints
    username_schema = z.string().min(3).max(20)
    print(f"Username (3-20 chars): {username_schema.parse('john_doe')}")
    
    # Exact length
    code_schema = z.string().length(6)
    print(f"6-char code: {code_schema.parse('ABC123')}")
    
    # Empty string handling
    optional_string = z.string().optional()
    print(f"Optional string (None): {optional_string.parse(None)}")
    
    print()


def email_validation_examples():
    """Demonstrate email validation."""
    print("=== Email Validation ===")
    
    # Basic email validation
    email_schema = z.string().email()
    
    valid_emails = [
        "user@example.com",
        "test.email+tag@domain.co.uk",
        "user.name@subdomain.example.org",
        "simple@test.io",
        "a@b.co"
    ]
    
    for email in valid_emails:
        result = email_schema.parse(email)
        print(f"✅ Valid email: {result}")
    
    # Email with length constraints
    business_email = z.string().min(5).max(50).email()
    print(f"Business email: {business_email.parse('contact@company.com')}")
    
    # Test invalid emails
    invalid_emails = [
        "invalid-email",
        "@example.com",
        "user@",
        "user@domain",
        "user.domain.com"
    ]
    
    print("\nInvalid emails (will show errors):")
    for email in invalid_emails:
        try:
            email_schema.parse(email)
        except z.ZodError as e:
            print(f"❌ {email}: {e}")
    
    print()


def url_validation_examples():
    """Demonstrate URL validation."""
    print("=== URL Validation ===")
    
    # Basic URL validation
    url_schema = z.string().url()
    
    valid_urls = [
        "https://example.com",
        "http://localhost:8000",
        "https://sub.domain.com/path?query=value",
        "http://127.0.0.1:3000/api/v1",
        "https://github.com/user/repo#readme"
    ]
    
    for url in valid_urls:
        result = url_schema.parse(url)
        print(f"✅ Valid URL: {result}")
    
    # URL with length constraints
    api_url = z.string().max(100).url()
    print(f"API URL: {api_url.parse('https://api.example.com/v1/users')}")
    
    # Test invalid URLs
    invalid_urls = [
        "not-a-url",
        "ftp://example.com",
        "http://",
        "https://"
    ]
    
    print("\nInvalid URLs (will show errors):")
    for url in invalid_urls:
        try:
            url_schema.parse(url)
        except z.ZodError as e:
            print(f"❌ {url}: {e}")
    
    print()


def regex_validation_examples():
    """Demonstrate regex pattern validation."""
    print("=== Regex Pattern Validation ===")
    
    # Phone number pattern
    phone_schema = z.string().regex(r'^\+?1?\d{9,15}$')
    valid_phones = ["+1234567890", "1234567890", "+12345678901"]
    for phone in valid_phones:
        print(f"✅ Valid phone: {phone_schema.parse(phone)}")
    
    # Alphanumeric code
    code_schema = z.string().regex(r'^[A-Z0-9]{6}$')
    print(f"Product code: {code_schema.parse('ABC123')}")
    
    # Password pattern (complex)
    password_schema = z.string().regex(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    )
    print(f"Strong password: {password_schema.parse('MyPass123!')}")
    
    # IP address pattern
    ip_schema = z.string().regex(r'^(\d{1,3}\.){3}\d{1,3}$')
    print(f"IP address: {ip_schema.parse('192.168.1.1')}")
    
    # Custom pattern with compiled regex
    hex_color = z.string().regex(re.compile(r'^#[0-9A-Fa-f]{6}$'))
    print(f"Hex color: {hex_color.parse('#FF5733')}")
    
    print()


def chained_validation_examples():
    """Demonstrate chaining multiple validations."""
    print("=== Chained String Validations ===")
    
    # Email with length constraints
    professional_email = (z.string()
                         .min(5)
                         .max(50)
                         .email())
    print(f"Professional email: {professional_email.parse('john.doe@company.com')}")
    
    # URL with pattern and length
    api_endpoint = (z.string()
                   .min(10)
                   .max(100)
                   .url()
                   .regex(r'.*\/api\/.*'))
    print(f"API endpoint: {api_endpoint.parse('https://example.com/api/v1/users')}")
    
    # Complex username validation
    username = (z.string()
               .min(3)
               .max(20)
               .regex(r'^[a-zA-Z0-9_]+$'))
    print(f"Username: {username.parse('john_doe_123')}")
    
    # Product SKU with multiple constraints
    sku = (z.string()
          .length(8)
          .regex(r'^[A-Z]{2}\d{6}$'))
    print(f"Product SKU: {sku.parse('AB123456')}")
    
    print()


def string_transformations():
    """Demonstrate string transformations."""
    print("=== String Transformations ===")
    
    # Basic transformations
    upper_schema = z.string().transform(str.upper)
    print(f"Uppercase: {upper_schema.parse('hello world')}")
    
    lower_schema = z.string().transform(str.lower)
    print(f"Lowercase: {lower_schema.parse('HELLO WORLD')}")
    
    # Chained transformations
    clean_schema = (z.string()
                   .transform(str.strip)
                   .transform(str.title))
    print(f"Clean and title: {clean_schema.parse('  hello world  ')}")
    
    # Custom transformation
    def normalize_phone(phone):
        # Remove all non-digits and add country code
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            return f"+1{digits}"
        return f"+{digits}"
    
    phone_normalizer = (z.string()
                       .regex(r'^[\d\s\-\(\)\+]+$')
                       .transform(normalize_phone))
    print(f"Normalized phone: {phone_normalizer.parse('(555) 123-4567')}")
    
    print()


def string_refinements():
    """Demonstrate custom string refinements."""
    print("=== String Refinements ===")
    
    # Custom validation with refinement
    no_profanity = z.string().refine(
        lambda x: 'badword' not in x.lower(),
        "Content contains inappropriate language"
    )
    print(f"Clean content: {no_profanity.parse('This is good content')}")
    
    # Multiple refinements
    secure_password = (z.string()
                      .min(8)
                      .refine(lambda x: any(c.isupper() for c in x), "Must contain uppercase")
                      .refine(lambda x: any(c.islower() for c in x), "Must contain lowercase")
                      .refine(lambda x: any(c.isdigit() for c in x), "Must contain digit")
                      .refine(lambda x: any(c in '!@#$%^&*' for c in x), "Must contain special char"))
    
    print(f"Secure password: {secure_password.parse('MySecure123!')}")
    
    # Business logic refinement
    valid_department = z.string().refine(
        lambda x: x.upper() in ['HR', 'IT', 'SALES', 'MARKETING', 'FINANCE'],
        "Invalid department code"
    )
    print(f"Department: {valid_department.parse('IT')}")
    
    print()


def error_handling_examples():
    """Demonstrate string validation error handling."""
    print("=== String Validation Error Handling ===")
    
    # Complex schema for demonstration
    complex_schema = (z.string()
                     .min(5)
                     .max(20)
                     .email()
                     .refine(lambda x: x.endswith('.com'), "Must be .com domain"))
    
    test_cases = [
        "ab",  # Too short
        "this-is-a-very-long-email-address@example.com",  # Too long
        "not-an-email",  # Not email format
        "valid@example.org",  # Wrong domain
        "good@example.com"  # Valid
    ]
    
    for test in test_cases:
        result = complex_schema.safe_parse(test)
        if result["success"]:
            print(f"✅ Valid: {result['data']}")
        else:
            print(f"❌ Invalid '{test}': {result['error']}")
    
    print()


def main():
    """Run all string validation examples."""
    print("Zodic String Validation Examples")
    print("=" * 50)
    
    basic_string_validation()
    email_validation_examples()
    url_validation_examples()
    regex_validation_examples()
    chained_validation_examples()
    string_transformations()
    string_refinements()
    error_handling_examples()
    
    print("=" * 50)
    print("All string validation examples completed!")


if __name__ == "__main__":
    main()
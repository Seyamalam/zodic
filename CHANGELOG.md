# Changelog

All notable changes to Zodic will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-26

### Added
- **New Schema Types**:
  - `literal()` schema for exact value matching
  - `enum()` schema for multiple choice validation
  - `date()` schema for date validation with string parsing
  - `datetime()` schema for datetime validation with string parsing

- **Enhanced String Validation**:
  - `email()` method for email format validation
  - `url()` method for URL format validation  
  - `regex()` method for custom pattern matching
  - Support for chaining multiple string validations

- **Enhanced Number Validation**:
  - Fixed `positive()` method to properly exclude zero
  - Better error messages for number validation
  - Improved precision in positive number checking

- **Union Operator Support**:
  - Added `|` operator for creating unions (`z.string() | z.number()`)
  - Fixed circular import issues in union implementation

- **Date/Time Features**:
  - Parse ISO format date/datetime strings
  - Parse common date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)
  - Date range validation with min/max constraints
  - Automatic datetime to date conversion

### Fixed
- **Critical Bugs**:
  - Fixed `positive()` validation to properly exclude zero
  - Fixed circular import in union operator
  - Improved error path handling in nested validations
  - Better type safety in schema cloning

- **Error Handling**:
  - More precise error messages
  - Better error path tracking in nested objects
  - Improved error aggregation

### Enhanced
- **Performance**:
  - Optimized schema cloning
  - Better validation pipeline
  - Reduced memory allocation in error handling

- **Type Safety**:
  - Better generic type inference
  - Improved IDE support and autocompletion
  - Stricter type checking

- **API Consistency**:
  - Consistent method chaining across all schema types
  - Better parameter validation
  - Improved documentation

### Examples
```python
import zodic as z

# New literal and enum schemas
theme_schema = z.enum(["light", "dark", "auto"])
status_schema = z.literal("active")

# Enhanced string validation
email_schema = z.string().email()
url_schema = z.string().url()
pattern_schema = z.string().regex(r"^[A-Z]{2,3}$")

# Date/datetime validation
date_schema = z.date().min(date(2024, 1, 1))
datetime_schema = z.datetime()

# Union operator
flexible_schema = z.string() | z.number() | z.boolean()

# Fixed positive validation
positive_schema = z.number().positive()  # Now properly excludes 0
```

### Breaking Changes
- None (fully backward compatible)

### Migration Guide
- All existing code continues to work without changes
- New features are opt-in and don't affect existing schemas
- The `positive()` method now correctly excludes zero (was a bug fix)

## [0.1.0] - 2025-06-25

### Added
- Initial release of Zodic
- Core validation framework with chainable API
- Primitive type validation (string, number, boolean, none)
- Collection type validation (object, array)
- Advanced features (transforms, refinements, optional/nullable)
- Comprehensive error handling with nested path reporting
- Zero dependencies core library
- Full type safety and IDE support
- 56 comprehensive tests with 85% coverage

### Features
- **String validation**: min/max length, exact length
- **Number validation**: min/max values, integer constraints, positive/negative
- **Object validation**: nested objects, optional fields, unknown key handling
- **Array validation**: element validation, length constraints
- **Error handling**: detailed error messages with proper paths
- **Transforms**: data transformation pipeline
- **Refinements**: custom validation logic
- **Type inference**: excellent IDE support


### API Highlights
```python
import zodic as z

# Basic validation
schema = z.string().min(3).max(10)
result = schema.parse("hello")

# Object validation
user_schema = z.object({
    'name': z.string(),
    'age': z.number().int().positive(),
    'email': z.string().optional()
})

# Advanced features
schema = z.string().transform(str.upper).refine(
    lambda x: x.startswith("HELLO"),
    "Must start with HELLO"
)
```
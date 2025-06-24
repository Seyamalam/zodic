# Changelog

All notable changes to Zodic will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
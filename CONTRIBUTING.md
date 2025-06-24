# Contributing to Zodic

Thank you for your interest in contributing to Zodic! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/zodic.git
   cd zodic
   ```

2. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests to ensure everything works**
   ```bash
   pytest tests/ -v
   ```

## 🧪 Development Workflow

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=zodic

# Run specific test file
pytest tests/test_primitives.py -v

# Run performance tests
python performance_test.py
```

### Code Quality
```bash
# Format code
black zodic tests

# Sort imports
isort zodic tests

# Type checking
mypy zodic

# Lint code
flake8 zodic
```

## 📝 Code Style

- **Follow PEP 8** style guidelines
- **Use type hints** for all functions and methods
- **Write docstrings** for all public functions using Google style
- **Keep line length** under 88 characters (Black default)
- **Use descriptive variable names** and avoid abbreviations

### Example Code Style
```python
def parse_value(self, value: Any, ctx: ValidationContext) -> str:
    """Parse and validate a string value.
    
    Args:
        value: The input value to validate
        ctx: Validation context for error reporting
        
    Returns:
        The validated string value
        
    Raises:
        ZodError: If validation fails
    """
    if not isinstance(value, str):
        raise ZodError([invalid_type_issue(value, "string", ctx)])
    return value
```

## 🧪 Testing Guidelines

### Test Structure
- **Unit tests**: Test individual functions and methods
- **Integration tests**: Test complete validation workflows
- **Error tests**: Test error handling and messages
- **Performance tests**: Benchmark critical paths

### Writing Tests
```python
def test_string_validation():
    """Test string validation with various inputs."""
    schema = z.string().min(3).max(10)
    
    # Test valid cases
    assert schema.parse("hello") == "hello"
    assert schema.parse("test") == "test"
    
    # Test invalid cases
    with pytest.raises(ZodError) as exc_info:
        schema.parse("hi")  # Too short
    assert "at least 3 characters" in str(exc_info.value)
    
    with pytest.raises(ZodError):
        schema.parse("toolongstring")  # Too long
```

### Test Coverage
- Aim for **85%+ test coverage**
- Test both **happy paths** and **error cases**
- Include **edge cases** and **boundary conditions**
- Test **error message content** and **paths**

## 🔧 Adding New Features

### 1. Plan the Feature
- Open a GitHub issue to discuss the feature
- Consider API design and backward compatibility
- Look at TypeScript Zod for inspiration

### 2. Implement the Feature
- Create feature branch: `git checkout -b feature/amazing-feature`
- Write the implementation with type hints
- Follow existing code patterns and style

### 3. Add Tests
- Write comprehensive tests for the new feature
- Test error cases and edge conditions
- Ensure all tests pass

### 4. Update Documentation
- Add docstrings to new functions
- Update README.md if needed
- Add examples to demonstrate usage

### 5. Submit Pull Request
- Write clear commit messages
- Include tests and documentation
- Reference related issues

## 🐛 Reporting Issues

### Bug Reports
Use the bug report template and include:
- **Python version** and **Zodic version**
- **Minimal reproduction example**
- **Expected vs actual behavior**
- **Full error messages** and stack traces

### Feature Requests
Use the feature request template and include:
- **Use case description**
- **Proposed API design**
- **Examples** of how it would be used
- **Comparison** with TypeScript Zod if applicable

## 📋 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch with descriptive name
3. **Make** your changes with tests
4. **Ensure** all tests pass and coverage is maintained
5. **Update** documentation if needed
6. **Commit** with clear, descriptive messages
7. **Push** to your fork
8. **Open** a Pull Request with detailed description

### PR Requirements
- ✅ All tests pass
- ✅ Code coverage maintained (85%+)
- ✅ Type checking passes (mypy)
- ✅ Code formatting applied (black, isort)
- ✅ Documentation updated if needed
- ✅ CHANGELOG.md updated for significant changes

## 🎯 Development Priorities

### Phase 2 (v0.2.0) - Enhanced Validators
- Email, URL, UUID validation for strings
- Regex pattern matching
- Date/time parsing
- More number validators (multipleOf, safe integers)

### Phase 3 (v0.3.0) - Advanced Features
- Recursive schemas and lazy evaluation
- Conditional validation
- Schema merging and composition
- Performance optimizations

### Phase 4 (v0.4.0) - Ecosystem Integration
- FastAPI integration
- Django integration
- Pydantic compatibility layer
- CLI tools

## 🤝 Community Guidelines

### Code of Conduct
- **Be respectful** and inclusive
- **Focus on constructive** feedback
- **Help others** learn and grow
- **Assume good intentions**
- **Follow the Golden Rule**

### Communication
- Use GitHub Issues for bugs and features
- Be clear and concise in descriptions
- Provide examples and context
- Search existing issues before creating new ones

## 🏆 Recognition

Contributors will be:
- Listed in the README.md contributors section
- Mentioned in release notes for significant contributions
- Invited to join the core team for sustained contributions

## 📚 Resources

- **TypeScript Zod**: https://github.com/colinhacks/zod
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **pytest Documentation**: https://docs.pytest.org/
- **PEP 8 Style Guide**: https://pep8.org/

Thank you for contributing to Zodic! Together we're building the best validation library for Python. 🚀
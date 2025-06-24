# Zodic Examples

This directory contains practical examples of using Zodic in different scenarios.

## Files

### `basic_usage.py`
Comprehensive examples of Zodic's core features:
- Basic type validation (string, number, boolean)
- Object and array validation
- Transformations and refinements
- Error handling
- API request validation

Run with:
```bash
python examples/basic_usage.py
```

### `fastapi_integration.py`
Example of integrating Zodic with FastAPI for API validation:
- Request/response validation
- Error handling middleware
- Custom validation decorators
- Real-world API endpoints

Run with:
```bash
pip install fastapi uvicorn
python examples/fastapi_integration.py
```

Then visit http://localhost:8000/docs for interactive API documentation.

## Example API Requests

### Create User
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice Johnson",
       "email": "alice@example.com",
       "age": 28,
       "preferences": {
         "theme": "dark",
         "notifications": true
       }
     }'
```

### Create Post
```bash
curl -X POST "http://localhost:8000/posts" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Getting Started with Zodic",
       "content": "zodic is a powerful validation library...",
       "tags": ["python", "validation"],
       "published": true
     }'
```

## More Examples

For more advanced examples and integrations, check out:
- [Django integration example](https://github.com/Seyamalam/zodic-django-example)
- [Flask integration example](https://github.com/Seyamalam/zodic-flask-example)
- [CLI validation example](https://github.com/Seyamalam/zodic-cli-example)
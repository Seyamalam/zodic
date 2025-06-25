#!/usr/bin/env python3
"""
FastAPI integration example with Zodic.

This example shows how to use Zodic for request/response validation in FastAPI.
"""

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
except ImportError:
    print("FastAPI not installed. Install with: pip install fastapi uvicorn")
    exit(1)

import zodic as z
from typing import Any, Dict

app = FastAPI(title="Zodic + FastAPI Example", version="1.0.0")

# Define schemas
UserCreateSchema = z.object({
    "name": z.string().min(1).max(100),
    "email": z.string().refine(lambda x: "@" in x and "." in x, "Invalid email format"),
    "age": z.number().int().min(13).max(120),
    "preferences": z.object({
        "theme": z.enum(["light", "dark"]).default("light"),
        "notifications": z.boolean().default(True)
    }).optional()
})

UserResponseSchema = z.object({
    "id": z.number().int(),
    "name": z.string(),
    "email": z.string(),
    "age": z.number().int(),
    "preferences": z.object({
        "theme": z.string(),
        "notifications": z.boolean()
    }),
    "created_at": z.string()
})

PostCreateSchema = z.object({
    "title": z.string().min(1).max(200),
    "content": z.string().min(10),
    "tags": z.array(z.string().min(1)).max(10).default([]),
    "published": z.boolean().default(False)
})

# Validation middleware
def validate_json(schema: z.Schema[Any]):
    """Decorator to validate request JSON with Zodic schema."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Get request data (this is simplified - in real FastAPI you'd use dependency injection)
            request_data = kwargs.get('data')
            if request_data is None:
                raise HTTPException(status_code=400, detail="Request body required")
            
            try:
                validated_data = schema.parse(request_data)
                kwargs['data'] = validated_data
                return await func(*args, **kwargs)
            except z.ZodError as e:
                raise HTTPException(status_code=422, detail=str(e))
        return wrapper
    return decorator

# In-memory storage (for demo purposes)
users_db: Dict[int, Dict[str, Any]] = {}
posts_db: Dict[int, Dict[str, Any]] = {}
next_user_id = 1
next_post_id = 1

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Zodic + FastAPI Integration Example"}

@app.post("/users")
async def create_user(data: dict):
    """Create a new user with Zodic validation."""
    global next_user_id
    
    try:
        # Validate input data
        validated_data = UserCreateSchema.parse(data)
        
        # Create user
        user = {
            "id": next_user_id,
            "name": validated_data["name"],
            "email": validated_data["email"],
            "age": validated_data["age"],
            "preferences": validated_data.get("preferences", {
                "theme": "light",
                "notifications": True
            }),
            "created_at": "2024-12-19T10:00:00Z"
        }
        
        users_db[next_user_id] = user
        next_user_id += 1
        
        # Validate response data
        response_data = UserResponseSchema.parse(user)
        return response_data
        
    except z.ZodError as e:
        raise HTTPException(status_code=422, detail={
            "message": "Validation failed",
            "errors": e.format()
        })

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    try:
        # Validate response data
        response_data = UserResponseSchema.parse(user)
        return response_data
    except z.ZodError as e:
        # This shouldn't happen if our data is consistent
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/posts")
async def create_post(data: dict):
    """Create a new post with Zodic validation."""
    global next_post_id
    
    try:
        # Validate input data
        validated_data = PostCreateSchema.parse(data)
        
        # Create post
        post = {
            "id": next_post_id,
            "title": validated_data["title"],
            "content": validated_data["content"],
            "tags": validated_data["tags"],
            "published": validated_data["published"],
            "created_at": "2024-12-19T10:00:00Z"
        }
        
        posts_db[next_post_id] = post
        next_post_id += 1
        
        return post
        
    except z.ZodError as e:
        raise HTTPException(status_code=422, detail={
            "message": "Validation failed",
            "errors": e.format()
        })

@app.get("/posts")
async def list_posts():
    """List all posts."""
    return {"posts": list(posts_db.values())}

# Error handler for validation errors
@app.exception_handler(z.ZodError)
async def zod_error_handler(request, exc: z.ZodError):
    """Global error handler for ZodError."""
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "errors": exc.format(),
            "details": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    print("Starting FastAPI server with Zodic validation...")
    print("Visit http://localhost:8000/docs for interactive API documentation")
    print("\nExample requests:")
    print("POST /users")
    print('{"name": "Alice", "email": "alice@example.com", "age": 25}')
    print("\nPOST /posts")
    print('{"title": "Hello Zodic", "content": "This is a test post with Zodic validation"}')
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
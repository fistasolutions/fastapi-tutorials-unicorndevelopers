from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom exception
class CustomException(Exception):
    def __init__(self, name: str, code: int, message: str):
        self.name = name
        self.code = code
        self.message = message

# Models with detailed documentation
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    full_name: Optional[str] = Field(None, description="The full name of the user")
    age: Optional[int] = Field(None, ge=0, le=120, description="The age of the user")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "age": 30
            }
        }

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="The password of the user")

class User(UserBase):
    id: int = Field(..., description="The unique identifier of the user")
    created_at: datetime = Field(..., description="The creation timestamp of the user")
    is_active: bool = Field(True, description="Whether the user is active")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "age": 30,
                "created_at": "2024-01-01T00:00:00",
                "is_active": True
            }
        }

# Initialize FastAPI with custom documentation
app = FastAPI(
    title="FastAPI Documentation Example",
    description="""
    This is a sample API that demonstrates how to create detailed API documentation
    and handle errors in FastAPI.
    
    ## Features
    * Detailed API documentation
    * Custom error handling
    * Request validation
    * Response models
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Error handlers
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"Custom error occurred: {exc.message}")
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.name,
            "message": exc.message,
            "path": request.url.path
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "path": request.url.path
        }
    )

# Routes with detailed documentation
@app.post(
    "/users/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information",
    response_description="The created user",
    tags=["users"]
)
async def create_user(user: UserCreate):
    """
    Create a new user with the following information:
    
    - **email**: The email address of the user
    - **full_name**: The full name of the user (optional)
    - **age**: The age of the user (optional)
    - **password**: The password of the user (minimum 8 characters)
    
    Returns the created user with additional information:
    
    - **id**: The unique identifier of the user
    - **created_at**: The creation timestamp
    - **is_active**: Whether the user is active
    """
    try:
        # Simulate user creation
        return User(
            id=1,
            email=user.email,
            full_name=user.full_name,
            age=user.age,
            created_at=datetime.now(),
            is_active=True
        )
    except Exception as e:
        raise CustomException(
            name="UserCreationError",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )

@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Retrieve a user by their unique identifier",
    response_description="The requested user",
    tags=["users"]
)
async def get_user(user_id: int):
    """
    Get a user by their ID.
    
    - **user_id**: The unique identifier of the user
    
    Returns the user if found, otherwise raises a 404 error.
    """
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return User(
        id=user_id,
        email="user@example.com",
        full_name="John Doe",
        age=30,
        created_at=datetime.now(),
        is_active=True
    ) 
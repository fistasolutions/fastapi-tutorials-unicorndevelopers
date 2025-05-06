from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
import pytest
from httpx import AsyncClient
import asyncio
from datetime import datetime
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import os
import json
import coverage
from unittest.mock import Mock, patch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Database dependency
def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create FastAPI app
app = FastAPI(
    title="FastAPI Testing Example",
    description="Example of testing and CI/CD with FastAPI",
    version="1.0.0"
)

# Helper functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Routes
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

# Test configuration
@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Unit tests
def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

@pytest.mark.asyncio
async def test_create_user(async_client, test_db):
    response = await async_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user(async_client, test_db):
    # Create test user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    create_response = await async_client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Get user
    response = await async_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

@pytest.mark.asyncio
async def test_create_item(async_client, test_db):
    # Create test user
    user_response = await async_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]

    # Create item
    item_data = {
        "name": "Test Item",
        "description": "Test Description",
        "price": 29.99
    }
    response = await async_client.post(
        "/items/",
        params={"user_id": user_id},
        json=item_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert data["owner_id"] == user_id

# Integration tests
@pytest.mark.integration
async def test_user_item_workflow(async_client, test_db):
    # Create user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    user_response = await async_client.post("/users/", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    # Create multiple items
    items_data = [
        {"name": "Item 1", "description": "Desc 1", "price": 10.99},
        {"name": "Item 2", "description": "Desc 2", "price": 20.99}
    ]
    for item_data in items_data:
        response = await async_client.post(
            "/items/",
            params={"user_id": user_id},
            json=item_data
        )
        assert response.status_code == 200

    # Get all items
    response = await async_client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["owner_id"] == user_id for item in data)

# Mock tests
def test_external_service(mocker):
    mock_service = mocker.patch("requests.get")
    mock_service.return_value.json.return_value = {"status": "success"}
    
    # Example of using the mock
    import requests
    response = requests.get("http://external-service.com/api")
    assert response.json()["status"] == "success"

# Example GitHub Actions workflow
"""
name: FastAPI CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run tests with coverage
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: ${{secrets.HEROKU_APP_NAME}}
        heroku_email: ${{secrets.HEROKU_EMAIL}}
"""

# Example Docker configuration
"""
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""

# Example pytest configuration
"""
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    integration: mark a test as an integration test
    unit: mark a test as a unit test

# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///./test.db")

@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db(TestingSessionLocal):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
""" 
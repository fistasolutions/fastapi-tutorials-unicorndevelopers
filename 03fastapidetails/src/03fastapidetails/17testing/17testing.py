from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import List, Optional
import pytest
from unittest.mock import Mock, patch

app = FastAPI()

# Models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Database simulation
fake_items_db = {
    1: {"id": 1, "name": "Item 1", "description": "Description 1", "price": 10.5},
    2: {"id": 2, "name": "Item 2", "description": "Description 2", "price": 20.0}
}

# Dependencies
def get_db():
    return fake_items_db

# Routes
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: dict = Depends(get_db)):
    items = list(db.values())
    return items[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: dict = Depends(get_db)):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

@app.post("/items/", response_model=Item)
def create_item(item: Item, db: dict = Depends(get_db)):
    if item.id in db:
        raise HTTPException(status_code=400, detail="Item already exists")
    db[item.id] = item.dict()
    return item

# Test client
client = TestClient(app)

# Unit tests
def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Item 1"

def test_read_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404

def test_create_item():
    item_data = {
        "id": 3,
        "name": "Item 3",
        "description": "Description 3",
        "price": 30.0
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Item 3"

# Integration tests
@pytest.fixture
def test_db():
    return {
        1: {"id": 1, "name": "Test Item 1", "price": 10.0},
        2: {"id": 2, "name": "Test Item 2", "price": 20.0}
    }

def test_integration_read_items(test_db):
    with patch("__main__.get_db", return_value=test_db):
        response = client.get("/items/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Test Item 1"

# Mock example
def test_mock_external_service():
    mock_service = Mock()
    mock_service.get_data.return_value = {"data": "mocked data"}
    
    with patch("__main__.external_service", mock_service):
        response = client.get("/external-data/")
        assert response.status_code == 200
        assert response.json()["data"] == "mocked data"

# Parametrized tests
@pytest.mark.parametrize(
    "item_id,expected_status,expected_name",
    [
        (1, 200, "Item 1"),
        (2, 200, "Item 2"),
        (999, 404, None)
    ]
)
def test_read_item_parametrized(item_id, expected_status, expected_name):
    response = client.get(f"/items/{item_id}")
    assert response.status_code == expected_status
    if expected_name:
        assert response.json()["name"] == expected_name 
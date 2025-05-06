from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

# Database simulation
fake_items_db = {
    "1": {"name": "Item 1", "price": 10.5},
    "2": {"name": "Item 2", "price": 20.0},
    "3": {"name": "Item 3", "price": 15.0}
}

class Item(BaseModel):
    name: str
    price: float

# Common dependencies
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Dependency for getting item
async def get_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return fake_items_db[item_id]

# Dependency for verifying token
async def verify_token(token: str = Depends(lambda x: x.headers.get("X-Token"))):
    if token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# Routes using dependencies
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/items/{item_id}")
async def read_item(item: dict = Depends(get_item)):
    return item

@app.post("/items/", dependencies=[Depends(verify_token)])
async def create_item(item: Item):
    item_id = str(len(fake_items_db) + 1)
    fake_items_db[item_id] = item.dict()
    return {"item_id": item_id, **item.dict()}

# Class-based dependency
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/paginated/")
async def read_items_paginated(pagination: Pagination = Depends()):
    items = list(fake_items_db.values())
    return items[pagination.skip : pagination.skip + pagination.limit] 
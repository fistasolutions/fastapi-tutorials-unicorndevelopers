from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List

app = FastAPI()

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Simulate user creation
    return {
        "id": 1,
        "email": user.email,
        "is_active": user.is_active,
        "items": []
    }

@app.get("/users/", response_model=List[User])
async def read_users():
    # Simulate user retrieval
    return [
        {
            "id": 1,
            "email": "user@example.com",
            "is_active": True,
            "items": []
        }
    ]

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    # Simulate user retrieval
    return {
        "id": user_id,
        "email": "user@example.com",
        "is_active": True,
        "items": []
    }

@app.post("/users/{user_id}/items/", response_model=Item)
async def create_item_for_user(user_id: int, item: ItemCreate):
    # Simulate item creation
    return {
        "id": 1,
        "title": item.title,
        "description": item.description,
        "owner_id": user_id
    } 
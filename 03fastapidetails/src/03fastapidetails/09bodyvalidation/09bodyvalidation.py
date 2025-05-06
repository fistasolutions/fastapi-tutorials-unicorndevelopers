from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    tax: Optional[float] = Field(None, gt=0)

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

@app.post("/items/")
async def create_item(
    item: Item = Body(..., embed=True),
    user: User = Body(..., embed=True)
):
    return {"item": item, "user": user}

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    )
):
    return {"item_id": item_id, "item": item} 
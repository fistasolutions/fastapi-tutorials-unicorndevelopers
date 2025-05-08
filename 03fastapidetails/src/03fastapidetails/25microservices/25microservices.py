from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx
import logging
from typing import List, Optional
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models
class Toy(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class Order(BaseModel):
    id: int
    toy_id: int
    quantity: int
    status: str
    created_at: datetime

class Payment(BaseModel):
    id: int
    order_id: int
    amount: float
    status: str

# Toy Service
toy_app = FastAPI(title="Toy Service")

toy_db = {
    1: {"id": 1, "name": "Teddy Bear", "price": 29.99, "stock": 50},
    2: {"id": 2, "name": "Robot Kit", "price": 49.99, "stock": 30},
}

@toy_app.get("/toys/", response_model=List[Toy])
async def get_toys():
    return list(toy_db.values())

@toy_app.get("/toys/{toy_id}", response_model=Toy)
async def get_toy(toy_id: int):
    if toy_id not in toy_db:
        raise HTTPException(status_code=404, detail="Toy not found")
    return toy_db[toy_id]

@toy_app.put("/toys/{toy_id}/stock")
async def update_stock(toy_id: int, quantity: int):
    if toy_id not in toy_db:
        raise HTTPException(status_code=404, detail="Toy not found")
    toy_db[toy_id]["stock"] -= quantity
    return {"message": "Stock updated"}

# Order Service
order_app = FastAPI(title="Order Service")

order_db = {}
order_counter = 0

@order_app.post("/orders/", response_model=Order)
async def create_order(toy_id: int, quantity: int):
    global order_counter
    order_counter += 1
    
    # Check toy availability
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8001/toys/{toy_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Toy not found")
        toy = response.json()
        
        if toy["stock"] < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")
        
        # Update stock
        await client.put(f"http://localhost:8001/toys/{toy_id}/stock?quantity={quantity}")
    
    # Create order
    order = {
        "id": order_counter,
        "toy_id": toy_id,
        "quantity": quantity,
        "status": "pending",
        "created_at": datetime.now()
    }
    order_db[order_counter] = order
    
    # Process payment
    async with httpx.AsyncClient() as client:
        payment_data = {
            "order_id": order_counter,
            "amount": toy["price"] * quantity
        }
        await client.post("http://localhost:8003/payments/", json=payment_data)
    
    return order

@order_app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    if order_id not in order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_db[order_id]

# Payment Service
payment_app = FastAPI(title="Payment Service")

payment_db = {}
payment_counter = 0

@payment_app.post("/payments/", response_model=Payment)
async def create_payment(order_id: int, amount: float):
    global payment_counter
    payment_counter += 1
    
    payment = {
        "id": payment_counter,
        "order_id": order_id,
        "amount": amount,
        "status": "completed"
    }
    payment_db[payment_counter] = payment
    
    # Update order status
    async with httpx.AsyncClient() as client:
        order_data = {"status": "paid"}
        await client.put(f"http://localhost:8002/orders/{order_id}", json=order_data)
    
    return payment

@payment_app.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int):
    if payment_id not in payment_db:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment_db[payment_id]

# Run services on different ports:
# uvicorn toy_service:toy_app --port 8001
# uvicorn order_service:order_app --port 8002
# uvicorn payment_service:payment_app --port 8003 
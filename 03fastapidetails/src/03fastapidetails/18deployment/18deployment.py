from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="FastAPI Deployment Example",
    description="Example of a FastAPI application ready for deployment",
    version="1.0.0"
)

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

# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Deployment Example",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    items = list(fake_items_db.values())
    return items[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Dockerfile content (as a comment for reference)
"""
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# docker-compose.yml content (as a comment for reference)
"""
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
"""

# nginx.conf content (as a comment for reference)
"""
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
"""

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    ) 
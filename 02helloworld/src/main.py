from fastapi import FastAPI

# Create a FastAPI app - like building a new restaurant!
app = FastAPI()

# This is our first API endpoint - like a menu item in our restaurant
@app.get("/")
async def root():
    return {"message": "Hello World"} 
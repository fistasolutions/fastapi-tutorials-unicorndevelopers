# 📚 FastAPI Documentation Adventure

## What This Code Does (Big Picture)
Imagine you're creating a magical recipe book for your toy store! This code helps us create a super-detailed guide that tells everyone how to use our store's special features. It's like having a friendly map that shows visitors where everything is and how to use all the magical tools in our store! 

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, EmailStr
```
This brings in our special documentation tools:
- FastAPI for our magical store
- Tools to create beautiful maps (documentation)
- Tools to check if visitors are following the rules
- Tools to make our store look professional

## Step 2: Creating Our Store Rules 📋
```python
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    full_name: Optional[str] = Field(None, description="The full name of the user")
    age: Optional[int] = Field(None, ge=0, le=120, description="The age of the user")
```
This creates our store rules that:
- Tell visitors what information they need to provide
- Make sure the information is correct
- Help visitors understand what each field means
- Show examples of how to fill out forms

## Step 3: Making Our Store Guide 🗺️
```python
app = FastAPI(
    title="FastAPI Documentation Example",
    description="""
    This is a sample API that demonstrates how to create detailed API documentation
    and handle errors in FastAPI.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
```
This creates our store guide that:
- Has a beautiful cover page
- Explains what our store does
- Shows different ways to read the guide
- Makes it easy to find information

## Step 4: Creating Our Store Doors 🚪
```python
@app.post("/users/")
async def create_user(user: UserCreate):
    """
    Create a new user with the following information:
    - email: The email address of the user
    - full_name: The full name of the user
    - age: The age of the user
    - password: The password of the user
    """
```
This creates our store doors that:
- Tell visitors how to enter
- Explain what information they need
- Show what will happen when they enter
- Help them understand what to expect

## Final Summary 📌
✅ We created a beautiful store guide
✅ We made clear rules for visitors
✅ We added helpful examples
✅ We made everything easy to understand

## Try It Yourself! 🚀
1. Make sure you have Python installed on your computer
2. Install FastAPI with all the standard tools using uv:
   ```
   uv add "fastapi[standard]"
   ```
3. Save the code in a file named `20apidocumentation.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 20apidocumentation.py
   ```
5. Visit these special pages:
   - `http://127.0.0.1:8000/docs` for the interactive guide
   - `http://127.0.0.1:8000/redoc` for the beautiful guide
   - `http://127.0.0.1:8000/openapi.json` for the technical guide

## What You'll Learn 🧠
- How to create beautiful documentation
- How to make your store easy to understand
- How to help visitors use your store
- How to make everything look professional

## Fun Things to Try! 🎮
1. Add more examples to your guide
2. Create different types of store rules
3. Add more store doors
4. Make your guide more colorful

## Cool Features! ✨
- Interactive documentation
- Beautiful store guide
- Clear rules and examples
- Professional looking store

Happy coding! 🎉 Remember, good documentation is like having a friendly guide who helps everyone understand how to use your magical toy store! 
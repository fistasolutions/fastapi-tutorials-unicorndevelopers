# 🌟 FastAPI Cookie Parameters Adventure

## What This Code Does (Big Picture)
Imagine you have a magical toy store where you can remember what toys each visitor likes! This code shows how to use cookies, which are like little memory cards that your website gives to visitors. It's like giving each visitor a special card that remembers their favorite toys and settings!

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, Cookie
from typing import Annotated
```
This line brings in FastAPI and Cookie, which helps us work with those special memory cards.

## Step 2: Creating Our Digital Toy Store 🏪
```python
app = FastAPI()
```
This creates our digital toy store where we'll keep our items.

## Step 3: Making Our Cookie Reader 🍪
```python
@app.get("/items/")
async def read_items(
    last_visited: Annotated[str | None, Cookie()] = None,
    favorite_toy: Annotated[str | None, Cookie()] = None
):
    return {
        "last_visited": last_visited,
        "favorite_toy": favorite_toy
    }
```
This creates a special way to read cookies:
- `last_visited` remembers when someone last visited the store
- `favorite_toy` remembers what toy they liked best
- Both are optional (that's what `None` means)

## Step 4: Creating Our Cookie Setter 🎯
```python
@app.post("/items/{item_id}")
async def create_item_cookie(item_id: str):
    response = {"message": f"Cookie set for item {item_id}"}
    return response
```
This creates a special way to save cookies:
- `item_id` is the toy they're looking at
- It saves this information in their cookie

## Final Summary 📌
✅ We created a website that can remember visitor preferences
✅ We learned how to read and write cookies
✅ We can store information about what visitors like
✅ We can make our website remember things about each visitor

## Try It Yourself! 🚀
1. Make sure you have Python installed on your computer
2. Install FastAPI with all the standard tools using uv:
   ```
   uv add "fastapi[standard]"
   ```
3. Save the code in a file named `13cookieparameters.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 13cookieparameters.py
   ```
5. Visit `http://127.0.0.1:8000/docs` and try:
   - Reading cookies (GET /items/)
   - Setting cookies (POST /items/{item_id})
   - Looking at your browser's cookies to see what was saved!

## What You'll Learn 🧠
- How to work with cookies in FastAPI
- How to remember visitor preferences
- How to read cookie values
- How to set new cookies

## Fun Things to Try! 🎮
1. Add more types of cookies
2. Store different kinds of information
3. Set expiration times for cookies
4. Create cookies with different settings

## Cool Features! ✨
- The website automatically creates documentation for you! Visit `http://127.0.0.1:8000/docs` to see it
- It can remember things about each visitor
- It works like a magical memory card
- It helps make your website more personal for each visitor

Happy coding! 🎉 Remember, cookies are like magical memory cards that help your website remember things about each visitor! 
# 🌟 FastAPI Query Parameters Adventure

## What This Code Does (Big Picture)
Imagine you have a magical toy store where you can ask for toys with different colors and sizes! This code creates a website that can show different items based on special questions in the URL. It's like having a smart toy store clerk who can find exactly what you're looking for!

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI
from typing import Optional
```
This line brings in FastAPI and some special tools to help us handle optional questions.

## Step 2: Creating Our Digital Toy Store 🏪
```python
app = FastAPI()
```
This creates our digital toy store where we'll keep our items.

## Step 3: Making Our Smart Item Finder 🔍
```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```
This creates a special way to find items:
- `@app.get("/items/")` means "when someone asks for items"
- `skip: int = 0` is like saying "start from the first toy" (but you can change it!)
- `limit: int = 10` is like saying "show me 10 toys" (but you can ask for more or less!)
- The `?` in the URL is like asking a question to the toy store clerk

## Final Summary 📌
✅ We created a website that can handle special questions in the URL
✅ We learned how to make optional parameters
✅ We can skip items and limit how many we see
✅ We can customize our search without changing the code

## Try It Yourself! 🚀
1. Make sure you have Python installed on your computer
2. Install FastAPI with all the standard tools using uv:
   ```
   uv add "fastapi[standard]"
   ```
3. Save the code in a file named `05queryparameters.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 05queryparameters.py
   ```
5. Try visiting these URLs in your browser:
   - `http://127.0.0.1:8000/items/` (Shows default values)
   - `http://127.0.0.1:8000/items/?skip=5` (Skips first 5 items)
   - `http://127.0.0.1:8000/items/?limit=3` (Shows only 3 items)
   - `http://127.0.0.1:8000/items/?skip=2&limit=5` (Skips 2, shows 5)

## What You'll Learn 🧠
- How to create query parameters in your URLs
- How to make parameters optional with default values
- How to combine multiple parameters
- How to customize your search without changing the code

## Fun Things to Try! 🎮
1. Add more query parameters (like color or size)
2. Change the default values
3. Try different combinations of parameters
4. Add a search parameter to find specific items

## Cool Features! ✨
- The website automatically creates documentation for you! Visit `http://127.0.0.1:8000/docs` to see it
- You can customize your search right in the URL
- It's super fast and easy to use
- You can combine different parameters to get exactly what you want

Happy coding! 🎉 Remember, query parameters are like having a magical shopping list that helps you find exactly what you're looking for in your digital store! 
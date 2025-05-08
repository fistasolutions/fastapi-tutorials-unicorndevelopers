# 🌟 FastAPI Header Parameters Adventure

## What This Code Does (Big Picture)
Imagine you have a magical toy store where toys come with special secret messages in their packaging! This code shows how to work with HTTP headers, which are like invisible notes that come with every request to your website. It's like having a secret message system for your digital toy store!

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, Header
from typing import Annotated
```
This line brings in FastAPI and Header, which helps us work with those invisible messages.

## Step 2: Creating Our Digital Toy Store 🏪
```python
app = FastAPI()
```
This creates our digital toy store where we'll keep our items.

## Step 3: Making Our Header Reader 📨
```python
@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None
):
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }
```
This creates a special way to read headers:
- `user_agent` tells us what kind of browser or app is being used
- `accept_language` tells us what language the visitor prefers
- Both are optional (that's what `None` means)

## Step 4: Creating Our Custom Header Handler 🎯
```python
@app.get("/custom-header/")
async def read_custom_header(
    x_toy_store_token: Annotated[str | None, Header()] = None
):
    return {"X-Toy-Store-Token": x_toy_store_token}
```
This creates a special way to handle custom headers:
- `x_toy_store_token` is our own special secret message
- It's like having a secret password in the message

## Final Summary 📌
✅ We created a website that can read invisible messages
✅ We learned how to work with HTTP headers
✅ We can get information about visitors' browsers
✅ We can create our own custom headers

## Try It Yourself! 🚀
1. Make sure you have Python installed on your computer
2. Install FastAPI with all the standard tools using uv:
   ```
   uv add "fastapi[standard]"
   ```
3. Save the code in a file named `14headerparameters.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 14headerparameters.py
   ```
5. Visit `http://127.0.0.1:8000/docs` and try:
   - Reading standard headers (GET /items/)
   - Setting custom headers (GET /custom-header/)
   - Look at the headers your browser sends automatically!

## What You'll Learn 🧠
- How to work with HTTP headers
- How to read browser information
- How to create custom headers
- How to handle different types of headers

## Fun Things to Try! 🎮
1. Add more types of headers
2. Create your own custom headers
3. Try different header combinations
4. See what headers your browser sends

## Cool Features! ✨
- The website automatically creates documentation for you! Visit `http://127.0.0.1:8000/docs` to see it
- It can read invisible messages from browsers
- It works with standard and custom headers
- It helps you understand what information browsers send

Happy coding! 🎉 Remember, headers are like invisible messages that help your website understand more about its visitors! 
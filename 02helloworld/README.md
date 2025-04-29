# Your First FastAPI App! 🎉

Hey there! 👋 Let's create your very first FastAPI application. It's like building your first digital restaurant! 🏪

## Installation 🛠️

First, let's install the required packages using `uv` (a super fast Python package installer!):

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment (like a special room for our project)
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install the required packages
uv pip install -e .
```

## Running the Program 🏃‍♂️

To start your digital restaurant, use this magic spell:

```bash
uv run fastapi dev src/main.py
```

Your computer will say something like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

This means your restaurant is open! You can visit it at `http://127.0.0.1:8000` in your web browser. 🏪

## What We're Building 🏗️

We're going to create a super simple app that says "Hello World" when someone visits it. It's like having a friendly robot that waves and says hi! 🤖

## Let's Look at the Code! 👀

Here's our simple code in `src/main.py`:

```python
from fastapi import FastAPI

# Create a FastAPI app - like building a new restaurant!
app = FastAPI()

# This is our first API endpoint - like a menu item in our restaurant
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Let's break it down line by line:

1. `from fastapi import FastAPI` - This is like getting our restaurant building kit! 🧰
2. `app = FastAPI()` - We're building our restaurant! 🏗️
3. `@app.get("/")` - This is like putting up a sign that says "Welcome!" at the front door 🚪
4. `async def root():` - This is our friendly robot that will greet visitors 🤖
5. `return {"message": "Hello World"}` - This is what our robot says when someone visits! 👋

## How to Run It 🏃‍♂️

1. Open your terminal (like a magic wand for computers! 🪄)
2. Type this magic spell:
   ```bash
   fastapi dev src/main.py
   ```
3. Your computer will say something like:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

## Let's Test It! 🧪

1. Open your web browser (like a magic window! 🪟)
2. Type this address: `http://127.0.0.1:8000`
3. You should see: `{"message": "Hello World"}`

## Cool Extra Features! 🌟

FastAPI gives us some amazing free stuff:

1. **Automatic Documentation** 📚
   - Visit `http://127.0.0.1:8000/docs` to see a cool interactive documentation page
   - It's like having a digital menu that explains everything!

2. **Alternative Documentation** 📖
   - Visit `http://127.0.0.1:8000/redoc` for another way to see the documentation
   - It's like having two different menus to choose from!

## Fun Quiz! 🎯

1. What does `@app.get("/")` do?
   - A) Makes a sandwich
   - B) Creates a welcome sign for our API
   - C) Paints the wall blue

2. What happens when you visit `http://127.0.0.1:8000`?
   - A) You get a pizza
   - B) You see `{"message": "Hello World"}`
   - C) Your computer turns into a robot

3. What's the coolest thing about FastAPI?
   - A) It makes your computer fly
   - B) It automatically creates documentation
   - C) It can make coffee

(Answers: 1-B, 2-B, 3-B) 😉

## What's Next? 🚀

Now that you've built your first API, you're ready to:
- Add more endpoints (like more menu items!)
- Make it do more interesting things
- Build your own digital restaurant!

Remember: Every great programmer started with a "Hello World"! 🌍

# 🎮 FastAPI Versioning Adventure

## What This Code Does (Big Picture)
Imagine you have a magical toy store that gets upgraded over time! Just like how video games have different versions (like Minecraft 1.0 and 2.0), our store needs different versions too. This code helps us create two magical doors to our store: one for the original version (v1) and another for the new upgraded version (v2)! 

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
```
This brings in our special tools:
- FastAPI for our magical store
- APIRouter for creating different store entrances
- BaseModel for organizing our toy information

## Step 2: Creating Our Toy Catalogs 📚
```python
class ItemV1(ItemBase):
    id: int
    created_at: datetime

class ItemV2(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []
    stock: int = Field(ge=0)
```
This creates two different toy catalogs:
- Version 1: Basic toy information
- Version 2: Extra cool features like:
  - When the toy was last updated
  - Special tags for each toy
  - How many toys are in stock

## Step 3: Making Different Store Entrances 🚪
```python
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v2_router = APIRouter(prefix="/v2", tags=["v2"])
```
This creates two magical doors:
- The v1 door for the original store
- The v2 door for the upgraded store
- Each door shows different toy information

## Step 4: Adding Special Features 🌟
```python
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'version']
)
```
This adds special features that:
- Count how many visitors use each door
- Track how fast we can show toys
- Make sure everything works perfectly

## Final Summary 📌
✅ We created two store versions
✅ We made different toy catalogs
✅ We built separate entrances
✅ We added special tracking features

## Try It Yourself! 🚀
1. Make sure you have Python installed
2. Install FastAPI with all the standard tools using uv:
   ```
   uv add "fastapi[standard]" prometheus-client prometheus-fastapi-instrumentator
   ```
3. Save the code in a file named `22apiversioning.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 22apiversioning.py
   ```
5. Try these magical doors:
   - Original Store (v1): `http://127.0.0.1:8000/v1/items/`
   - Upgraded Store (v2): `http://127.0.0.1:8000/v2/items/`
   - Health Check: `http://127.0.0.1:8000/health`
   - Store Statistics: `http://127.0.0.1:8000/metrics`

## What You'll Learn 🧠
- How to create different versions of your store
- How to show different information in each version
- How to track store visitors
- How to keep everything organized

## Fun Things to Try! 🎮
1. Compare what you see in v1 and v2
2. Add new features to the v2 store
3. Create a v3 store with your own ideas
4. Watch how many people visit each version

## Cool Features! ✨
- Two different store versions
- Special tracking tools
- Health checking
- Detailed toy information

## Differences Between Versions 🔄
### Version 1 (Original Store):
- Basic toy information
- Simple and easy to use
- Perfect for beginners

### Version 2 (Upgraded Store):
- More toy details
- Tags for finding toys easily
- Stock information
- Last update time

Happy coding! 🎉 Remember, API versioning is like having different versions of your favorite video game - each new version adds cool new features while keeping the old version available for those who like it! 
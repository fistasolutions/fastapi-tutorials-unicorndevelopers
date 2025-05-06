from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from typing import List, Optional
from pydantic import BaseModel
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

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

# Redis configuration
REDIS_URL = "redis://localhost:6379"

# Startup event
@app.on_event("startup")
async def startup():
    # Initialize Redis connection
    redis_client = redis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    
    # Initialize FastAPI Cache with Redis backend
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    
    # Initialize Rate Limiter
    await FastAPILimiter.init(redis_client)

# Caching example
@app.get("/items/", response_model=List[Item])
@cache(expire=60)  # Cache for 60 seconds
async def read_items():
    logger.info("Fetching items from database")
    return list(fake_items_db.values())

@app.get("/items/{item_id}", response_model=Item)
@cache(expire=30)  # Cache for 30 seconds
async def read_item(item_id: int):
    logger.info(f"Fetching item {item_id} from database")
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]

# Rate limiting example
@app.get("/limited/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def limited_route():
    return {"message": "This is a rate-limited route"}

@app.get("/limited-by-ip/", dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def limited_by_ip(request: Request):
    return {
        "message": "This is a rate-limited route by IP",
        "client_ip": request.client.host
    }

# Custom rate limiter
async def custom_rate_limiter(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    # Get current count from Redis
    count = await FastAPILimiter.redis.get(key)
    
    if count and int(count) >= 3:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )
    
    # Increment count
    await FastAPILimiter.redis.incr(key)
    # Set expiry if first request
    if not count:
        await FastAPILimiter.redis.expire(key, 60)

@app.get("/custom-limited/", dependencies=[Depends(custom_rate_limiter)])
async def custom_limited_route():
    return {"message": "This is a custom rate-limited route"}

# Cache invalidation example
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # Add item to database
    fake_items_db[item.id] = item.dict()
    
    # Invalidate cache
    await FastAPICache.clear(namespace="items")
    
    return item

# Cache key builder example
def custom_key_builder(
    func,
    namespace: str = "",
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__name__}:{args}:{kwargs}"
    return cache_key

@app.get("/custom-cache/")
@cache(expire=60, key_builder=custom_key_builder)
async def custom_cached_route(param: str):
    return {"message": f"This is a custom cached route with param: {param}"}

# Middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response 
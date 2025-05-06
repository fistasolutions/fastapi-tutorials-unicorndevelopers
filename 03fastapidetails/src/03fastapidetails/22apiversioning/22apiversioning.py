from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import logging
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'version']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint', 'version']
)

# Base models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# V1 models
class ItemV1(ItemBase):
    id: int
    created_at: datetime

# V2 models
class ItemV2(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []
    stock: int = Field(ge=0)

# Database simulation
fake_items_db_v1 = {
    1: {"id": 1, "name": "Item 1", "description": "Description 1", "price": 10.5, "created_at": datetime.now()}
}

fake_items_db_v2 = {
    1: {
        "id": 1,
        "name": "Item 1",
        "description": "Description 1",
        "price": 10.5,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "tags": ["new", "featured"],
        "stock": 100
    }
}

# Create routers for different versions
v1_router = APIRouter(prefix="/v1", tags=["v1"])
v2_router = APIRouter(prefix="/v2", tags=["v2"])

# V1 endpoints
@v1_router.get("/items/", response_model=List[ItemV1])
async def read_items_v1():
    REQUEST_COUNT.labels(method="GET", endpoint="/items", version="v1").inc()
    with REQUEST_LATENCY.labels(method="GET", endpoint="/items", version="v1").time():
        logger.info("Fetching items from v1 database")
        return list(fake_items_db_v1.values())

@v1_router.get("/items/{item_id}", response_model=ItemV1)
async def read_item_v1(item_id: int):
    REQUEST_COUNT.labels(method="GET", endpoint="/items/{item_id}", version="v1").inc()
    with REQUEST_LATENCY.labels(method="GET", endpoint="/items/{item_id}", version="v1").time():
        logger.info(f"Fetching item {item_id} from v1 database")
        if item_id not in fake_items_db_v1:
            raise HTTPException(status_code=404, detail="Item not found")
        return fake_items_db_v1[item_id]

# V2 endpoints
@v2_router.get("/items/", response_model=List[ItemV2])
async def read_items_v2():
    REQUEST_COUNT.labels(method="GET", endpoint="/items", version="v2").inc()
    with REQUEST_LATENCY.labels(method="GET", endpoint="/items", version="v2").time():
        logger.info("Fetching items from v2 database")
        return list(fake_items_db_v2.values())

@v2_router.get("/items/{item_id}", response_model=ItemV2)
async def read_item_v2(item_id: int):
    REQUEST_COUNT.labels(method="GET", endpoint="/items/{item_id}", version="v2").inc()
    with REQUEST_LATENCY.labels(method="GET", endpoint="/items/{item_id}", version="v2").time():
        logger.info(f"Fetching item {item_id} from v2 database")
        if item_id not in fake_items_db_v2:
            raise HTTPException(status_code=404, detail="Item not found")
        return fake_items_db_v2[item_id]

# Create main app
app = FastAPI(
    title="FastAPI Versioning Example",
    description="Example of API versioning with FastAPI",
    version="1.0.0"
)

# Include version routers
app.include_router(v1_router)
app.include_router(v2_router)

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Middleware for logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response 
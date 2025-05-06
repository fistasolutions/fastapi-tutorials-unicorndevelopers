from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_client import Counter, Histogram, generate_latest
from typing import List, Optional, Dict
import logging
import time
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import redis
import requests
from pydantic import BaseModel
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./analytics.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis configuration
REDIS_URL = "redis://localhost:6379"
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Jaeger configuration
JAEGER_HOST = "localhost"
JAEGER_PORT = 6831

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

# Models
class APIMetric(Base):
    __tablename__ = "api_metrics"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    method = Column(String, index=True)
    status_code = Column(Integer)
    response_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    request_headers = Column(JSON)
    response_headers = Column(JSON)
    client_ip = Column(String)

# Pydantic models
class MetricResponse(BaseModel):
    endpoint: str
    method: str
    avg_response_time: float
    requests_per_minute: float
    success_rate: float
    error_rate: float

class EndpointStats(BaseModel):
    total_requests: int
    avg_response_time: float
    success_rate: float
    error_rate: float
    requests_by_method: Dict[str, int]
    status_code_distribution: Dict[str, int]

# Setup OpenTelemetry
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name=JAEGER_HOST,
    agent_port=JAEGER_PORT,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Get tracer
tracer = trace.get_tracer(__name__)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create FastAPI app
app = FastAPI(
    title="FastAPI Distributed Tracing Example",
    description="Example of distributed tracing and API analytics with FastAPI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument SQLAlchemy
SQLAlchemyInstrumentor().instrument(
    engine=engine,
    service="sqlite",
)

# Instrument Redis
RedisInstrumentor().instrument()

# Instrument requests
RequestsInstrumentor().instrument()

# Create database tables
Base.metadata.create_all(bind=engine)

# Middleware for request tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    # Store request data
    metric = APIMetric(
        endpoint=request.url.path,
        method=request.method,
        status_code=response.status_code,
        response_time=duration,
        request_headers=dict(request.headers),
        response_headers=dict(response.headers),
        client_ip=request.client.host
    )

    db = SessionLocal()
    db.add(metric)
    db.commit()
    db.close()

    return response

# Analytics endpoints
@app.get("/analytics/metrics", response_model=List[MetricResponse])
async def get_metrics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    with tracer.start_as_current_span("get_metrics") as span:
        query = db.query(APIMetric)
        
        if start_time:
            span.set_attribute("start_time", start_time.isoformat())
            query = query.filter(APIMetric.timestamp >= start_time)
        
        if end_time:
            span.set_attribute("end_time", end_time.isoformat())
            query = query.filter(APIMetric.timestamp <= end_time)

        metrics = query.all()
        
        # Group metrics by endpoint and method
        grouped_metrics = {}
        for metric in metrics:
            key = (metric.endpoint, metric.method)
            if key not in grouped_metrics:
                grouped_metrics[key] = []
            grouped_metrics[key].append(metric)

        # Calculate statistics
        results = []
        for (endpoint, method), endpoint_metrics in grouped_metrics.items():
            total_requests = len(endpoint_metrics)
            avg_response_time = sum(m.response_time for m in endpoint_metrics) / total_requests
            success_count = sum(1 for m in endpoint_metrics if m.status_code < 400)
            error_count = total_requests - success_count
            
            # Calculate requests per minute
            if start_time and end_time:
                minutes = (end_time - start_time).total_seconds() / 60
            else:
                minutes = 1
            
            requests_per_minute = total_requests / minutes if minutes > 0 else 0
            
            results.append(
                MetricResponse(
                    endpoint=endpoint,
                    method=method,
                    avg_response_time=avg_response_time,
                    requests_per_minute=requests_per_minute,
                    success_rate=success_count / total_requests if total_requests > 0 else 0,
                    error_rate=error_count / total_requests if total_requests > 0 else 0
                )
            )

        return results

@app.get("/analytics/endpoint/{endpoint}", response_model=EndpointStats)
async def get_endpoint_stats(
    endpoint: str,
    db: Session = Depends(get_db)
):
    with tracer.start_as_current_span("get_endpoint_stats") as span:
        span.set_attribute("endpoint", endpoint)
        
        metrics = db.query(APIMetric).filter(APIMetric.endpoint == endpoint).all()
        
        if not metrics:
            return EndpointStats(
                total_requests=0,
                avg_response_time=0,
                success_rate=0,
                error_rate=0,
                requests_by_method={},
                status_code_distribution={}
            )

        total_requests = len(metrics)
        avg_response_time = sum(m.response_time for m in metrics) / total_requests
        success_count = sum(1 for m in metrics if m.status_code < 400)
        error_count = total_requests - success_count

        # Count requests by method
        requests_by_method = {}
        for metric in metrics:
            requests_by_method[metric.method] = requests_by_method.get(metric.method, 0) + 1

        # Count status codes
        status_code_distribution = {}
        for metric in metrics:
            status = str(metric.status_code)
            status_code_distribution[status] = status_code_distribution.get(status, 0) + 1

        return EndpointStats(
            total_requests=total_requests,
            avg_response_time=avg_response_time,
            success_rate=success_count / total_requests,
            error_rate=error_count / total_requests,
            requests_by_method=requests_by_method,
            status_code_distribution=status_code_distribution
        )

# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Example endpoints to generate traces and metrics
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user_id", user_id)
        
        # Simulate external service call
        with tracer.start_as_current_span("external_service_call"):
            time.sleep(0.1)  # Simulate latency
            
            # Cache check
            with tracer.start_as_current_span("cache_check"):
                cached_user = redis_client.get(f"user:{user_id}")
                if cached_user:
                    return json.loads(cached_user)
            
            # Database query
            with tracer.start_as_current_span("database_query"):
                time.sleep(0.05)  # Simulate database query
                user = {"id": user_id, "name": f"User {user_id}"}
                
                # Cache result
                redis_client.setex(
                    f"user:{user_id}",
                    timedelta(minutes=5),
                    json.dumps(user)
                )
                
                return user

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    with tracer.start_as_current_span("get_order") as span:
        span.set_attribute("order_id", order_id)
        
        # Simulate microservice calls
        with tracer.start_as_current_span("get_order_details"):
            time.sleep(0.1)
            order = {"id": order_id, "status": "processing"}
            
        with tracer.start_as_current_span("get_user_details"):
            user_id = order_id % 100
            response = requests.get(f"http://localhost:8000/users/{user_id}")
            user = response.json()
            
        order["user"] = user
        return order

# Example usage and testing:
"""
# Start Jaeger
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.22

# Start Redis
docker run -d --name redis -p 6379:6379 redis

# Test endpoints
curl http://localhost:8000/users/1
curl http://localhost:8000/orders/1

# View traces
Open http://localhost:16686 in your browser

# View metrics
curl http://localhost:8000/metrics
curl http://localhost:8000/analytics/metrics
curl http://localhost:8000/analytics/endpoint/users/1
""" 
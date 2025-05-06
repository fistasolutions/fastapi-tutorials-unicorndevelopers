from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
import aio_pika
import json
import logging
from datetime import datetime
import asyncio
from functools import wraps
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = "sqlite+aiosqlite:///./events.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Redis configuration
REDIS_URL = "redis://localhost:6379"
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# RabbitMQ configuration
RABBITMQ_URL = "amqp://guest:guest@localhost/"

# Models
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    payload = Column(JSON)
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

# Pydantic models
class EventBase(BaseModel):
    event_type: str
    payload: Dict

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    status: str
    created_at: datetime
    processed_at: Optional[datetime]

    class Config:
        orm_mode = True

# Message queue connection
async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

# Database dependency
async def get_db():
    async with async_session() as session:
        yield session

# Event publisher
class EventPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        if not self.connection:
            self.connection = await get_rabbitmq_connection()
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                "events", aio_pika.ExchangeType.TOPIC
            )

    async def publish(self, event_type: str, payload: dict):
        await self.connect()
        message = aio_pika.Message(
            body=json.dumps({"event_type": event_type, "payload": payload}).encode()
        )
        await self.exchange.publish(message, routing_key=event_type)
        logger.info(f"Published event: {event_type}")

    async def close(self):
        if self.connection:
            await self.connection.close()

# Event consumer
class EventConsumer:
    def __init__(self, queue_name: str, routing_key: str):
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        if not self.connection:
            self.connection = await get_rabbitmq_connection()
            self.channel = await self.connection.channel()
            
            # Declare exchange
            exchange = await self.channel.declare_exchange(
                "events", aio_pika.ExchangeType.TOPIC
            )
            
            # Declare queue
            self.queue = await self.channel.declare_queue(
                self.queue_name, durable=True
            )
            
            # Bind queue to exchange
            await self.queue.bind(exchange, routing_key=self.routing_key)

    async def consume(self, callback):
        await self.connect()
        
        async def process_message(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    event = json.loads(message.body.decode())
                    await callback(event)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    # Requeue message
                    await message.reject(requeue=True)

        await self.queue.consume(process_message)
        logger.info(f"Started consuming from queue: {self.queue_name}")

    async def close(self):
        if self.connection:
            await self.connection.close()

# Event handlers
async def handle_order_created(event: dict):
    logger.info(f"Processing order created event: {event}")
    # Implement order processing logic
    await asyncio.sleep(1)  # Simulate processing
    logger.info("Order processed successfully")

async def handle_payment_completed(event: dict):
    logger.info(f"Processing payment completed event: {event}")
    # Implement payment confirmation logic
    await asyncio.sleep(1)  # Simulate processing
    logger.info("Payment confirmed successfully")

# Create FastAPI app
app = FastAPI(
    title="FastAPI Event-Driven Architecture Example",
    description="Example of event-driven architecture with FastAPI",
    version="1.0.0"
)

# Event publisher instance
publisher = EventPublisher()

# Startup event
@app.on_event("startup")
async def startup_event():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Start event consumers
    order_consumer = EventConsumer("orders", "order.*")
    payment_consumer = EventConsumer("payments", "payment.*")
    
    asyncio.create_task(order_consumer.consume(handle_order_created))
    asyncio.create_task(payment_consumer.consume(handle_payment_completed))

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    await publisher.close()

# Routes
@app.post("/events/", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # Create event in database
    db_event = Event(
        event_type=event.event_type,
        payload=event.payload,
        status="pending"
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)

    # Publish event to message queue
    background_tasks.add_task(
        publisher.publish,
        event.event_type,
        event.payload
    )

    return db_event

@app.get("/events/", response_model=List[EventResponse])
async def get_events(
    event_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = db.query(Event)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    events = await query.all()
    return events

@app.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Example usage:
"""
# Create an order
event = {
    "event_type": "order.created",
    "payload": {
        "order_id": "123",
        "user_id": "456",
        "items": [
            {"item_id": "789", "quantity": 2}
        ],
        "total_amount": 29.99
    }
}

# Process payment
event = {
    "event_type": "payment.completed",
    "payload": {
        "order_id": "123",
        "payment_id": "xyz",
        "amount": 29.99,
        "status": "success"
    }
}
""" 
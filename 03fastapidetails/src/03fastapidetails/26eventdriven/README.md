# 📬 FastAPI Event-Driven Adventure

## What This Code Does (Big Picture)
Imagine you're running a magical toy store where different parts of the store can send messages to each other using magical mailboxes! When something happens (like a new toy order), it sends a magical letter that other parts of the store can read and respond to. It's like having a team of helpful elves who each have their own special job and communicate through magical messages! 

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, BackgroundTasks
import aio_pika
import redis.asyncio as redis
```
This brings in our special tools:
- FastAPI for our magical store
- RabbitMQ (aio_pika) for our magical mailboxes
- Redis for our quick-memory storage
- Special tools to keep track of messages

## Step 2: Creating Our Message System 📨
```python
class EventPublisher:
    async def publish(self, event_type: str, payload: dict):
        # Sends magical messages
```
This creates our magical message system that:
- Writes special messages (events)
- Puts them in magical mailboxes
- Makes sure they get delivered
- Keeps track of all messages

## Step 3: Making Our Message Readers 📭
```python
class EventConsumer:
    async def consume(self, callback):
        # Reads and processes messages
```
This creates our message readers that:
- Check magical mailboxes for new messages
- Read and understand the messages
- Do special tasks based on the messages
- Send responses when needed

## Step 4: Setting Up Special Tasks ✨
```python
async def handle_order_created(event: dict):
    # Handle new toy orders
async def handle_payment_completed(event: dict):
    # Handle completed payments
```
This creates special helpers that:
- Process new toy orders
- Handle payments
- Update toy inventory
- Send confirmation messages

## Final Summary 📌
✅ We created magical mailboxes
✅ We made message senders
✅ We set up message readers
✅ We organized special tasks

## Try It Yourself! 🚀
1. Make sure you have Python installed
2. Install FastAPI and message tools using uv:
   ```
   uv add "fastapi[standard]" aio-pika redis sqlalchemy[asyncio] aiosqlite
   ```
3. Install and start RabbitMQ and Redis:
   ```
   # Start RabbitMQ
   rabbitmq-server
   # Start Redis
   redis-server
   ```
4. Save the code in a file named `26eventdriven.py`
5. Run the website using uv:
   ```
   uv run fastapi dev 26eventdriven.py
   ```
6. Try these magical messages:

### Send a New Order Message 📮
```json
{
    "event_type": "order.created",
    "payload": {
        "order_id": "123",
        "items": [{"name": "Teddy Bear", "quantity": 1}]
    }
}
```

### Send a Payment Message 💰
```json
{
    "event_type": "payment.completed",
    "payload": {
        "order_id": "123",
        "amount": 29.99
    }
}
```

## What You'll Learn 🧠
- How to send magical messages
- How to read and process messages
- How to organize different tasks
- How to make parts work together

## Fun Things to Try! 🎮
1. Create different types of messages
2. Watch how messages flow
3. Add new message handlers
4. See how tasks work together

## Cool Features! ✨
- Magical message system
- Automatic task handling
- Message tracking
- Safe message delivery

## Special Powers You Get 🌟
### Message Sending:
- Create new messages
- Choose message types
- Add special information
- Track message status

### Message Reading:
- Get messages automatically
- Process different message types
- Handle tasks in order
- Keep everything organized

## Example Message Flow 🔄
1. Customer orders a toy:
   - Order message is created
   - Stock is checked
   - Payment is requested

2. Payment is completed:
   - Payment message is sent
   - Order is updated
   - Confirmation is sent

Happy coding! 🎉 Remember, event-driven architecture is like having a team of magical elves who communicate through special mailboxes to get their work done together! 
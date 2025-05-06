from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class Notification(BaseModel):
    message: str
    email: str
    priority: Optional[str] = "normal"

# Simulated email sending function
def send_email(email: str, message: str):
    logger.info(f"Sending email to {email}")
    # Simulate email sending delay
    time.sleep(2)
    logger.info(f"Email sent to {email}: {message}")

# Simulated notification processing
def process_notification(notification: Notification):
    logger.info(f"Processing notification: {notification.message}")
    # Simulate processing delay
    time.sleep(3)
    logger.info(f"Notification processed: {notification.message}")

# Simulated database update
def update_database(item_id: int, status: str):
    logger.info(f"Updating database for item {item_id}")
    # Simulate database update delay
    time.sleep(1)
    logger.info(f"Database updated for item {item_id} with status: {status}")

@app.post("/notifications/")
async def create_notification(
    notification: Notification, background_tasks: BackgroundTasks
):
    # Add email sending to background tasks
    background_tasks.add_task(
        send_email, notification.email, notification.message
    )
    
    # Add notification processing to background tasks
    background_tasks.add_task(process_notification, notification)
    
    return {
        "message": "Notification will be sent in the background",
        "notification": notification
    }

@app.post("/items/{item_id}/status")
async def update_item_status(
    item_id: int, status: str, background_tasks: BackgroundTasks
):
    # Add database update to background tasks
    background_tasks.add_task(update_database, item_id, status)
    
    return {
        "message": "Status update will be processed in the background",
        "item_id": item_id,
        "status": status
    }

@app.post("/batch-process/")
async def batch_process(background_tasks: BackgroundTasks):
    # Add multiple tasks to background
    for i in range(5):
        background_tasks.add_task(
            send_email,
            f"user{i}@example.com",
            f"Batch processing notification {i}"
        )
    
    return {"message": "Batch processing started in the background"} 
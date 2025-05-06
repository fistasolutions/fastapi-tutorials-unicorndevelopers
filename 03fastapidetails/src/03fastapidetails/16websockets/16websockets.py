from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
from datetime import datetime

app = FastAPI()

# Connection manager
class ConnectionManager:
    def __init__(self):
        # Store active connections
        self.active_connections: Dict[str, List[WebSocket]] = {
            "chat": [],
            "notifications": []
        }

    async def connect(self, websocket: WebSocket, client_id: str, channel: str):
        await websocket.accept()
        self.active_connections[channel].append(websocket)
        # Notify others about new connection
        await self.broadcast(
            f"Client {client_id} joined the {channel} channel",
            channel,
            exclude=websocket
        )

    def disconnect(self, websocket: WebSocket, client_id: str, channel: str):
        self.active_connections[channel].remove(websocket)
        return f"Client {client_id} left the {channel} channel"

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, channel: str, exclude: WebSocket = None):
        for connection in self.active_connections[channel]:
            if connection != exclude:
                await connection.send_text(message)

manager = ConnectionManager()

# WebSocket endpoints
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id, "chat")
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "client_id": client_id,
                "message": data,
                "timestamp": datetime.now().isoformat()
            }
            await manager.broadcast(json.dumps(message), "chat")
    except WebSocketDisconnect:
        message = manager.disconnect(websocket, client_id, "chat")
        await manager.broadcast(message, "chat")

@app.websocket("/ws/notifications/{client_id}")
async def notification_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id, "notifications")
    try:
        while True:
            # Simulate receiving notifications
            await asyncio.sleep(5)
            notification = {
                "type": "notification",
                "message": f"New notification for {client_id}",
                "timestamp": datetime.now().isoformat()
            }
            await manager.send_personal_message(
                json.dumps(notification),
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id, "notifications")

# HTTP endpoint to send message to all connected clients
@app.post("/broadcast/{channel}")
async def broadcast_message(channel: str, message: str):
    await manager.broadcast(message, channel)
    return {"status": "Message broadcasted"}

# HTTP endpoint to send message to specific client
@app.post("/send/{client_id}")
async def send_message(client_id: str, message: str):
    # In a real application, you would need to maintain a mapping of client_ids to WebSocket connections
    return {"status": "Message sent"} 
# 🔐 FastAPI WebSocket Security Adventure

## What This Code Does (Big Picture)
Imagine you're creating a magical toy store chat room where friends can talk to each other safely! It's like having a special clubhouse with a security guard who makes sure only members with special badges can come in. Once inside, friends can chat and share messages instantly, like having magical walkie-talkies that work through the internet! 

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, WebSocket
from jose import jwt
from passlib.context import CryptContext
```
This brings in our special tools:
- FastAPI for our magical clubhouse
- WebSocket for our magical walkie-talkies
- Special tools to make secret badges (JWT tokens)
- Tools to keep passwords super safe

## Step 2: Creating Our Security System 🎫
```python
class User(Base):
    __tablename__ = "users"
    username = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)
```
This creates our security system that:
- Keeps track of all club members
- Stores special secret badges
- Makes sure each username is unique
- Keeps passwords extra safe with special magic

## Step 3: Making Our Chat Room Safe 🏰
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
```
This creates our safe chat system that:
- Knows who's in each chat room
- Makes sure messages go to the right friends
- Keeps track of who's talking
- Helps friends find each other

## Step 4: Adding Special Powers ✨
```python
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str
):
    # Verify token and connect
```
This adds magical powers that:
- Check special badges before letting friends in
- Keep chat rooms separate and safe
- Make sure messages are delivered instantly
- Help friends leave safely when they're done

## Final Summary 📌
✅ We created a safe chat clubhouse
✅ We made special security badges
✅ We built magical walkie-talkies
✅ We kept everything super secure

## Try It Yourself! 🚀
1. Make sure you have Python installed
2. Install FastAPI and security tools using uv:
   ```
   uv add "fastapi[standard]" python-jose[cryptography] passlib[bcrypt] sqlalchemy
   ```
3. Save the code in a file named `24websocketsecurity.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 24websocketsecurity.py
   ```
5. Try these magical steps:
   - Create a new account: `POST /users/`
   - Get your special badge: `POST /token`
   - Join a chat room: Connect to `/ws/{room_id}?token=your_badge`

## What You'll Learn 🧠
- How to make a safe chat room
- How to create special security badges
- How to send instant messages
- How to keep everything secure

## Fun Things to Try! 🎮
1. Create different chat rooms
2. Send messages to friends
3. Try joining with wrong badges
4. Watch messages appear instantly

## Cool Features! ✨
- Secure user accounts
- Special security badges (JWT tokens)
- Instant messaging (WebSockets)
- Safe chat rooms

## Security Features 🛡️
### For Club Members:
- Special username and password
- Secure login system
- Personal security badges
- Safe message delivery

### For Chat Rooms:
- Private room access
- Instant message delivery
- Secure connections
- Safe disconnections

## Example Chat Session 💭
1. Get your security badge:
```bash
curl -X POST "http://localhost:8000/token" -d "username=your_name&password=your_password"
```

2. Connect to a chat room:
```javascript
let ws = new WebSocket("ws://localhost:8000/ws/room1?token=your_badge");
```

3. Send a message:
```javascript
ws.send(JSON.stringify({
    "content": "Hello friends!",
    "room_id": "room1"
}));
```

Happy coding! 🎉 Remember, WebSocket security is like having a special clubhouse where only friends with the right badges can come in and chat safely! 
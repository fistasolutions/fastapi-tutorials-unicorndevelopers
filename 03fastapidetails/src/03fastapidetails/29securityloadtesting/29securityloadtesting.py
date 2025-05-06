from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List, Optional, Dict
import logging
import time
import json
from datetime import datetime, timedelta
import redis
import httpx
import asyncio
from pydantic import BaseModel, EmailStr, Field, IPvAnyAddress
import aioredis
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.backends.redis import RedisBackend
import locust
from locust import HttpUser, task, between

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Redis configuration
REDIS_URL = "redis://localhost:6379"
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rate limiting configuration
RATE_LIMIT_RULES = {
    "default": "100/minute",
    "login": "5/minute",
    "high_priority": "1000/minute"
}

# IP whitelist/blacklist
WHITELISTED_IPS = {"127.0.0.1", "10.0.0.0/8"}
BLACKLISTED_IPS = set()

# Security middleware
class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Check IP blacklist
        if client_ip in BLACKLISTED_IPS:
            return Response(
                status_code=status.HTTP_403_FORBIDDEN,
                content=json.dumps({"detail": "IP address is blacklisted"}),
                media_type="application/json"
            )

        # Add security headers
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = redis_client

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Get rate limit key
        path = request.url.path
        rate_limit_key = f"rate_limit:{client_ip}:{path}"
        
        # Get current count
        count = self.redis.get(rate_limit_key)
        if count is None:
            count = 0
        else:
            count = int(count)
        
        # Check rate limit
        limit = self.get_rate_limit(path)
        if count >= limit:
            return Response(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content=json.dumps({"detail": "Too many requests"}),
                media_type="application/json"
            )
        
        # Increment count
        self.redis.incr(rate_limit_key)
        if count == 0:
            self.redis.expire(rate_limit_key, 60)  # Expire after 1 minute
        
        return await call_next(request)

    def get_rate_limit(self, path: str) -> int:
        if path.startswith("/login"):
            return 5  # 5 requests per minute
        elif path.startswith("/api/v1"):
            return 1000  # 1000 requests per minute
        return 100  # Default: 100 requests per minute

# Create FastAPI app
app = FastAPI(
    title="FastAPI Security and Load Testing Example",
    description="Example of API Gateway security and load testing with FastAPI",
    version="1.0.0"
)

# Add middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "testserver"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Load testing with Locust
class UserBehavior(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Login and get token
        response = self.client.post("/token", {
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]

    @task(2)
    def get_user_profile(self):
        self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(1)
    def get_protected_resource(self):
        self.client.get(
            "/api/v1/protected",
            headers={"Authorization": f"Bearer {self.token}"}
        )

# Example load testing configuration
"""
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        # Login
        response = self.client.post("/token", {
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
    
    @task(3)
    def view_user_profile(self):
        self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def view_items(self):
        self.client.get(
            "/items",
            headers={"Authorization": f"Bearer {self.token}"}
        )

# Run with:
# locust -f locustfile.py --host=http://localhost:8000
"""

# Security best practices:
"""
1. Use HTTPS in production
2. Implement proper authentication and authorization
3. Use rate limiting to prevent abuse
4. Implement IP whitelisting/blacklisting
5. Add security headers
6. Use proper password hashing
7. Implement request validation
8. Use proper session management
9. Implement audit logging
10. Regular security updates
"""

# Load testing best practices:
"""
1. Define realistic test scenarios
2. Start with smoke tests
3. Gradually increase load
4. Monitor system resources
5. Test different endpoints
6. Include error scenarios
7. Test with different payload sizes
8. Monitor response times
9. Test with different concurrent users
10. Analyze results and optimize
""" 
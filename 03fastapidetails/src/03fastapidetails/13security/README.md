# 🌟 FastAPI Security Adventure

## What This Code Does (Big Picture)
Imagine you have a magical castle with special keys and secret passwords! This code helps us create a secure system where only people with the right magical keys can enter different rooms. It's like having a friendly dragon guard who checks if visitors have the right magical tokens before letting them in! 

## Step 1: Getting Our Magic Tools 🛠️
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
```
This brings in our special security tools:
- OAuth2 for creating magical tokens
- JWT for making special secret keys
- CryptContext for hiding passwords like magic spells!

## Step 2: Setting Up Our Castle Security 🏰
```python
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```
This creates our castle's security rules:
- A secret key that only our castle knows
- A special way to create magical tokens
- Tokens that expire after 30 minutes (like temporary magic!)

## Step 3: Creating Our User System 👥
```python
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
```
This creates our visitor system:
- Each visitor has a special username
- They can have an email and full name
- We can disable visitors if needed

## Step 4: Making Our Security Guards 🛡️
```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Creates magical tokens for visitors
```
These are our friendly security guards:
- They check if passwords are correct
- They create special magical tokens
- They make sure only the right people can enter

## Final Summary 📌
✅ We created a secure system for our castle
✅ We can give special magical tokens to visitors
✅ We can check if visitors are allowed to enter
✅ We can protect different rooms in our castle

## Try It Yourself! 🚀
1. Make sure you have Python installed on your computer
2. Install FastAPI with all the standard tools using uv:
   ```
   uv add "fastapi[standard]"
   ```
3. Save the code in a file named `13security.py`
4. Run the website using uv:
   ```
   uv run fastapi dev 13security.py
   ```
5. Visit `http://127.0.0.1:8000/docs` and try:
   - Getting a magical token (use username: johndoe, password: secret)
   - Using the token to access your profile
   - Trying to access without a token (it won't work!)

## What You'll Learn 🧠
- How to create secure passwords
- How to make magical tokens
- How to protect different parts of your castle
- How to check if visitors are allowed

## Fun Things to Try! 🎮
1. Create new types of visitors
2. Change how long tokens last
3. Add more protected rooms
4. Create different security levels

## Cool Features! ✨
- The website automatically checks magical tokens
- It keeps passwords safe using magic spells
- It can give temporary access to visitors
- It protects different parts of the castle

Happy coding! 🎉 Remember, security is like having friendly dragon guards who make sure only the right people can enter your magical castle! 
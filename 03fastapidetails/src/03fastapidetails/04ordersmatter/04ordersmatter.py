from fastapi import FastAPI

app = FastAPI()

@app.get("/user/me")
async def read_user_me():
    return {"username": "me"}

@app.get("/user/{username}")
async def read_user(username: str):
    return {"username": username}


@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]
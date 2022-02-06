from fastapi import FastAPI
import uvicorn, asyncio

from models import User
from configuration import admin
from base import database 

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def main():
    try:
        res = await User.add_user(User(**admin))
    except Exception as e:
        return {"error" : str(e)}
    else:
        return res

@app.post("/login")
async def login_user(user:User):
    return await User.login(user)


if __name__ == "__main__":
    uvicorn.run("main:app",
            host="0.0.0.0",port=10000,
            reload=True,workers =2, 
            ssl_keyfile='public/oleg.key', 
            ssl_certfile='public/oleg.crt',)



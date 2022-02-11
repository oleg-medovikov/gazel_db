from fastapi import FastAPI
import uvicorn, asyncio

from models import User, Login_json, New_user, Token, Info_user
from configuration import admin
from base import database 

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/login")
async def login_user(json : Login_json):
    "Процесс авторизации клиента"
    return await User.loging(json)

@app.post("/new_user")
async def add_user(json: New_user):
    """Процесс создания нового юзера.
    в айди записывается токен создателя,
    который нужно проверить на наличие админских прав"""
    res = await User.cheak_admin(json.token)
    if not res == True:
        return res
    else:
        try:
            res = await User.add_user(json)
        except Exception as e:
            return {"error" : str(e)}
        else:
            return res


@app.post("/users_list")
async def users_list(json : Token):
    "выдаем список существующих юзернеймов"
    res = await User.cheak_token(json.token)
    if not res == True:
        return res
    else:
        try:
            res = await User.list()
        except Exception as e:
            return {"error" : str(e)}
        else:
            return res


@app.post("/user_info")
async def user_info(json : Info_user):
    "Посмотреть информацию о конкретном пользователе"
    res = await User.cheak_token(json.token)
    if not res == True:
        return res
    else:
        try:
            res = await User.user_info(json.username)
        except Exception as e:
            return {"error" : str(e)}
        else:
            return res
   

#@app.post("/allow_projects")
#async def allow_projects(json : Project_access):
#    "Получение списка доступных пользователю проектов"
#    pass



@app.get("/")
async def main():
    "Для отладки, добавление админа"
    try:
        res = await User.add_user(New_user(**admin))
    except Exception as e:
        return {"error" : str(e)}
    else:
        return res

@app.get("/delete_admin")
async def delete_admin():
    "Для отладки, удаление админа"
    return await User.delete(User(**admin))



if __name__ == "__main__":
    uvicorn.run("main:app",
            host="0.0.0.0",port=10000,
            reload=True,workers =2, 
            ssl_keyfile='public/oleg.key', 
            ssl_certfile='public/oleg.crt',)



from .app import app

from typing import Optional
from fastapi import Header, Body
from models import User, Login_json, New_user, Update_password




@app.post("/login", tags=["users"])
async def login_user(json : Login_json):
    "Процесс авторизации клиента"
    return await User.loging(json)

@app.post("/new_user", tags=["users"])
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
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res

@app.get("/users_list", tags=["users"])
async def users_list(
        Authorization: Optional[str] = Header(None)
        ): 
    "выдаем список существующих юзернеймов"
    if Authorization is None:
        return None
    res = await User.cheak_token(Authorization)
    if not res == True:
        return res
    else:
        try:
            res = await User.list()
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res


@app.get("/user_info", tags=["users"])
async def user_info(
        Authorization: Optional[str] = Header(None),
        username: Optional[str] = Body(None)
        ):
    "Посмотреть информацию о конкретном пользователе"
    if Authorization is None or username is None:
        return None

    res = await User.cheak_token(Authorization)
    if not res == True:
        return res
    else:
        try:
            res = await User.user_info(username)
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res

   
@app.put("/update_password", tags=["users"])
async def user_update_password(
        json : Update_password
        ):
    "Сменить пароль пользователя, через токен админа"
    res = await User.cheak_admin(json.token)
    if not res == True:
        return res
    else:
        try:
            res = await User.update_password(json)
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res
 

@app.get("/delete_admin", tags=["users"])
async def delete_admin():
    "Для отладки, удаление админа, для обновления его настроек"
    return await User.delete(User(**admin))


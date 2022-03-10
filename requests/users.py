from .app import app

from typing import Optional
from fastapi import Header, Body
from models import User 




@app.get("/login", tags=["users"])
async def login_user(
        username: Optional[str] = Body(None),
        password_hash: Optional[str] = Body(None)
        ):
    "Процесс авторизации клиента"
    if username is None or password_hash is None:
        return None
    else:
        return await User.loging(username,password_hash)

@app.post("/new_user", tags=["users"])
async def add_user(
        Authorization: Optional[str] = Header(None),
        first_name: Optional[str] = Body(None),
        second_name: Optional[str] = Body(None),
        username: Optional[str] = Body(None),
        password_hash: Optional[str] = Body(None),
        position: Optional[str] = Body(None),
        admin: Optional[bool] = Body(None),
        ):
    """Процесс создания нового юзера.
    в айди записывается токен создателя,
    который нужно проверить на наличие админских прав"""
    if Authorization is None:
        return None

    res = await User.cheak_admin(Authorization)
    if not res == True:
        return res
    else:
        try:
            res = await User.add_user(
                    first_name,
                    second_name,
                    username,
                    password_hash,
                    position,
                    admin
                    )
        except Exception as e:
            return {"error" : str(e)}
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
        Authorization: Optional[str] = Header(None),
        username: Optional[str] = Body(None),
        password_hash: Optional[str] = Body(None)
        ):
    "Сменить пароль пользователя, через токен админа"
    res = await User.cheak_admin(Authorization)
    if not res == True:
        return res
    else:
        try:
            res = await User.update_password(username,password_hash)
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res
 

@app.get("/delete_admin", tags=["users"])
async def delete_admin():
    "Для отладки, удаление админа, для обновления его настроек"
    return await User.delete(User(**admin))


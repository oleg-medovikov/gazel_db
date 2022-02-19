from .app import app

from models import User, Login_json, New_user, Token, Info_user, Update_password

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

@app.post("/users_list", tags=["users"])
async def users_list(json : Token):
    "выдаем список существующих юзернеймов"
    res = await User.cheak_token(json.token)
    if not res == True:
        return res
    else:
        try:
            res = await User.list()
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res


@app.post("/user_info", tags=["users"])
async def user_info(json : Info_user):
    "Посмотреть информацию о конкретном пользователе"
    res = await User.cheak_token(json.token)
    if not res == True:
        return res
    else:
        try:
            res = await User.user_info(json.username)
        except Exception:
            return {"error" : str(Exception)}
        else:
            return res

   
@app.post("/update_password", tags=["users"])
async def user_update_password(json : Update_password):
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


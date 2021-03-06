from datetime import date
from uuid import uuid4, UUID
from pydantic import BaseModel, Field
from sqlalchemy import select

from base import database, table_users

class User(BaseModel):
    u_id: UUID = Field(default_factory=uuid4)
    first_name: str
    second_name: str
    username: str
    password_hash: str
    position: str
    admin: bool

    async def add_user(FIRST_NAME,SECOND_NAME,USERNAME,PASSWORD_HASH,POSITION,ADMIN):
        "процедура добавления пользователя"
        query = table_users.select(table_users.c.username == USERNAME )
        res = await database.fetch_one(query)
        if not res is None:
            return {"error" : f"Пользователь {username} уже существует" }
        else:

            values = {"u_id":uuid4(),
                      "first_name" : FIRST_NAME,
                      "second_name": SECOND_NAME,
                      "username": USERNAME,
                      "password_hash" : PASSWORD_HASH,
                      "position" : POSITION,
                      "admin" : ADMIN}
            query = table_users.insert().values(**values)
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Пользователь добавлен"}
    
    async def delete(User):
        "процедура удаления юзера Не используется"
        query = table_users.select(table_users.c.username == User.username)
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "Такого пользователя не существует"}
        else:
            query = table_users.delete(table_users.c.username == User.username)
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "okey"}

    async def loging(USERNAME, PASSWORD_HASH):
        "Процедура входа в систему"
        query = table_users.select(table_users.c.username == USERNAME )
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "Пользователь не найден в системе"}
        else:
            if not res["password_hash"] == PASSWORD_HASH:
                return { "error" : "Неправильный пароль"}
            else:
                TOKEN = uuid4().hex
                query = table_users.update()\
                        .where(table_users.c.username== USERNAME)\
                        .values(token = TOKEN)
                try:
                    await database.execute(query)
                except Exception as e:
                    return {"error" : str(e)}
                else:
                    return {"message" : "Вы успешно вошли в систему",
                            "first_name" : res["first_name"],
                            "second_name" : res["second_name"],
                            "position"    : res["position"],
                            "admin" : res["admin"],
                            "token" : TOKEN }

    async def update_password(USERNAME, PASSWORD_HASH):
        "Процедура обновления пароля"
        query = table_users.select(table_users.c.username == USERNAME )
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "Пользователь не найден в системе"}
        else:
            query = table_users.update()\
                     .where(table_users.c.username == USERNAME)\
                     .values(password_hash = PASSWORD_HASH)
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Пароль успешно сменён"}

    async def cheak_admin(TOKEN):
        "проверка токена на то, что он принадлежит админу"
        query = table_users.select(table_users.c.token == TOKEN)
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "недействительный токен"}
        else:
            if res["admin"] == False:
                return {"error" : "у пользователя недостаточно прав"}
            else:
                return True

    async def cheak_token(TOKEN):
        "проверка токена на актуальность"
        query = table_users.select(table_users.c.token == TOKEN)
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "недействительный токен"}
        else:
            return True

    async def list():
        "список пользователей"
        query = select([table_users.c.username])
        res = await database.fetch_all(query)
        if res is None:
            return {"error" : "Нет пользователей, что очень странно"}
        else:
            return res

    async def user_info(username: str):
        "посмотреть информацию о пользователе"
        query = table_users.select(table_users.c.username == username)
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "Такой пользователь не найден, что очень странно"}
        else:
            otvet = {**res}
            otvet.pop('u_id')
            otvet.pop('password_hash')
            otvet.pop('token')
            return otvet

    async def user_id(TOKEN_NAME):
        "возвращает идентификатор пользователя через токен"
        query = table_users.select( table_users.c.token == TOKEN_NAME )
        res = await database.fetch_one(query)

        if not res is None:
            return res['u_id']
        else:
            query = table_users.select( table_users.c.username == TOKEN_NAME )
            res = await database.fetch_one(query)

            if not res is None:
                return res['u_id']
            else:
                return None
    
    async def name_user(U_ID):
        "возвращает username пользователя через u_id"
        query = table_users.select(table_users.c.u_id == U_ID)
        res = await database.fetch_one(query)
        if res is None:
            raise  Exception("Такой пользователь не найден, что очень странно")
        else:
            return res['username']


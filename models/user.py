from datetime import date
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel, Field


from base import database, table_users

class User(BaseModel):
    u_id: UUID = Field(default_factory=uuid4)
    first_name: str
    second_name: str
    username: str
    password_hash: str
    position: str
    admin: bool

    async def add_user(User):
        "процедура добавления пользователя"
        query = table_users.select(table_users.c.username == User.username )
        res = await database.fetch_one(query)
        if not res is None:
            return {"error" : "Пользователь с таким username уже существует" }
        else:
            User.u_id = uuid4()
            values = {**User.dict()}
            query = table_users.insert().values(**values)
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Пользователь добавлен"}

    async def loging(User):
        "Процедура входа в систему"
        query = table_users.select(table_users.c.username == User.username )
        res = await database.fetch_one(query)
        if res is None:
            return {"error" : "Пользователь не найден в системе"}
        else:
            if not res.password_hash == User.password_hash:
                return { "error" : "Неправильный пароль"}
            else:
                token = uuid4().hex
                query = table_users.update().values(table_users.c.token==token)\
                        .where(table_users.c.username==User.username)
                try:
                    await database.execute(query)
                except Exception as e:
                    return {"error" : str(e)}
                else:
                    return {"message" : "Вы успешно вошли в систему",
                            "token" : token }



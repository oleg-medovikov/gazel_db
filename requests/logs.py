from .app import app
from fastapi import Header, Body
from typing import Optional

from models import User, User_log

@app.post('/create_log', tags=["logs"])
async def create_log(
    Authorization : Optional[str] = Header(None),
    P_ID : Optional[str] = Body(None),
    R_ID : Optional[str] = Body(None),
    EVENT : Optional[str] = Body(None)
        ):
    "Создание записи лога"
    if Authorization is None or \
            P_ID is None or \
            R_ID is None or \
            EVENT is None:
        return None

    "Проверка пользователя"
    U_ID = await User.user_id(Authorization)
    if U_ID is None:
        return {"error" : "Нет такого пользователя"}
    
    try:
        await User_log.create(P_ID, R_ID, U_ID, EVENT)
    except Exception as e:
        return {"error" : str(e)}
    else:
        return {"message" : "ok"}

@app.get('/list_log', tags=["logs"])
async def list_log(
    Authorization : Optional[str] = Header(None),
    ID : Optional[str] = Body(None)
        ):
    "Чтение лога"

    if Authorization is None or ID is None:
        return None

    "Проверка пользователя"
    U_ID = await User.user_id(Authorization)
    if U_ID is None:
        return {"error" : "Нет такого пользователя"}
 
    try:
        res = await User_log.list_events(ID)
    except Exception as e:
        return {"error" : str(e)}
    else:
        return res



from .app import app
from fastapi import Header, Body, File, UploadFile
from typing import Optional

from models import User, Object, Object_binary, Reference, Project_access

@app.post('/create_object', tags=["objects"])
async def create_object(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None),
    O_HASH_SUM : Optional[str] = Body(None),
    FILE_NAME :  Optional[str] = Body(None),
    file : UploadFile = File(...)
    ):
    "Создание нового объекта"
    "Проверка пользователя"
    U_ID = await User.user_id(Authorization)
    if U_ID is None:
        return {"error" : "Нет такого пользователя"}

    "Проверка обозначения"
    REFERENCE = await Reference.cheak(R_ID)
    if REFERENCE is None:
        return {"error" : "Нет такого обозначения"}

    "Проверка прав"
    ACCESS_LEVEL = await Project_access.access(U_ID, REFERENCE["p_id"])

    if ACCESS_LEVEL is None or ACCESS_LEVEL > 1:
        return {"error" : "Недостаточно прав"}
    
    "Создание объекта"
    res = await Object.create(
            REFERENCE["r_id"],
            U_ID,
            FILE_NAME,
            O_HASH_SUM
            )
    if 'error' in res:
        return res
        
    try:
        res = await Object_binary.create(res['O_ID'], file.file.read()) 
    except Exception as e:
        return {"error" : str(e)}
    else:
        return res
    
    


@app.get('/objects_list', tags=["objects"])
async def objects_list(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None)
    ):
    "Возвращает список файлов, принадлежащий обозначению"

    if Authorization is None or R_ID is None:
        return None

    return await Object.files(R_ID)



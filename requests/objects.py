from .app import app
from fastapi import Header, Body, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import Optional

from models import User, Object, Object_binary, Reference, Project_access, Object_file
from configuration import DATA_FILES

@app.post('/create_object', tags=["objects"])
async def create_object(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None),
    O_HASH_SUM : Optional[str] = Body(None),
    FILE_NAME :  Optional[str] = Body(None),
    file : UploadFile = File(...)
    ):
    "Создание нового объекта"
    if Authorization is None or \
            R_ID is None or \
            O_HASH_SUM is None or \
            FILE_NAME  is None or \
            file is None:
        return None

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
        return {"error" : "Недостаточно прав загрузки в базу"}
    
    "Создание объекта"
    res = await Object.create(
            REFERENCE["r_id"],
            U_ID,
            FILE_NAME,
            O_HASH_SUM
            )
    if 'error' in res:
        return res
    
    #res = await Object_binary.create(res['O_ID'], file.file) 
    return await Object_file.write(res['O_ID'], file) 

@app.put('/update_object', tags=['objects'])
async def update_object(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None),
    O_HASH_SUM : Optional[str] = Body(None),
    O_ID : Optional[str] = Body(None),
    file : UploadFile = File(...)
        ):
    "Создание нового объекта"
    if Authorization is None or \
            R_ID is None or \
            O_HASH_SUM is None or \
            O_ID is None or \
            file is None:
        return None

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
        return {"error" : "Недостаточно прав для обновления файла"}
 
    res = await Object.update_hash(O_ID,O_HASH_SUM)
    
    if "error" in res:
        return res

    try:
        #res = await Object_binary.update(O_ID, file.file)
        res = await Object_file.write(O_ID, file)
    except Exception as e:
        return {"error" : str(e)}
    else:
        return res

@app.get('/download_object', tags=['objects'])
async def download_object(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None),
    O_ID : Optional[str] = Body(None)
        ):
    "Выгрузка файла из базы"

    if Authorization is None or O_ID is None or R_ID is None:
        return None

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

    if ACCESS_LEVEL is None or ACCESS_LEVEL > 3:
        return {"error" : "Недостаточно прав для выгрузки файлов из базы"}

    try:
        #res = await Object_binary.read(O_ID)
        res = await Object_file.read(O_ID)
    except Exception as e:
        return {"error" : str(e)}
    else:
        return res 

@app.delete('/delete_object', tags=['objects'])
async def delete_object(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None),
    O_ID : Optional[str] = Body(None)
        ):
    "Удаление файла из базы"
    if Authorization is None or R_ID is None or O_ID is None:
            return None

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

    if ACCESS_LEVEL is None or ACCESS_LEVEL > 0:
        return {"error" : "Недостаточно прав для удаления файла"}

    return await Object_file.delete(O_ID)


#@app.get('/download_test')
#async def test_download():
#    #O_ID = '188d6720-b781-45a3-8c64-7cb63c1357ca'
#    O_ID = 'c6b4a86b-2e00-4f11-80c1-94d409bec259'
#    return await Object_file.read(O_ID)
#    try:
#        res = await Object_binary.read(O_ID)
#    except Exception as e:
#        return {"error" : str(e)}
#    else:
#        if 'error' in res:
#            return res
#        else:
#            return res


 
@app.get('/objects_list', tags=["objects"])
async def objects_list(
    Authorization : Optional[str] = Header(None),
    R_ID : Optional[str] = Body(None)
    ):
    "Возвращает список файлов, принадлежащий обозначению"

    if Authorization is None or R_ID is None:
        return None

    return await Object.files(R_ID)

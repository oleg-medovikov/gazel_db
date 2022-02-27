from .app import app
from fastapi import Header, Body
from typing import Optional

from models import User, Reference, Project, Project_access

@app.post('/create_reference', tags=["references"])
async def create_reference(
    Authorization : Optional[str] = Header(None),
    P_NAME : Optional[str] = Body(None),
    R_NAME : Optional[str] = Body(None),
    R_CODE_NAME_LEVEL_1 : Optional[str] = Body(None),
    R_CODE_NAME_LEVEL_2 : Optional[int] = Body(None),
    R_CODE_NAME_LEVEL_3 : Optional[int] = Body(None),
    ):
    """Создание наименования в рамках проекта"""

    if Authorization is None or \
       P_NAME is None or \
       R_NAME is None or \
       R_CODE_NAME_LEVEL_1 is None or \
       R_CODE_NAME_LEVEL_2 is None or \
       R_CODE_NAME_LEVEL_3 is None:
        return None

    # проверка пользователя
    U_ID = await User.user_id(Authorization) 
    if U_ID is None:
        return {"error" : "Такого пользователя не существует"}
   
    # проверка имени проекта 
    P_ID = await Project.id(P_NAME)
    if P_ID is None:
        return {"error" : "Такого проекта не существует"}

    # Проверка уровня прав
    ACCESS = await Project_access.access(U_ID,P_ID)
    
    if not ACCESS == 0:
        return {"error" : "У пользователя недостаточно прав"}

    # добавляем новое наименование
    
    return await Reference.create(
           P_ID, R_NAME,
           R_CODE_NAME_LEVEL_1,
           R_CODE_NAME_LEVEL_2,
           R_CODE_NAME_LEVEL_3
            )







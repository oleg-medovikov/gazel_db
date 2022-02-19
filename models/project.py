from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from base import database, table_projects

class New_project(BaseModel):
    token : str
    p_name : str
    p_description : str

class Project(BaseModel):
    p_id : UUID = Field(default_factory=uuid4)
    p_name : str
    p_description : str
    p_datacreate: datetime
    u_id : UUID = Field(default_factory=uuid4)

    async def create(author_id, json : New_project):
        "Процедура создания нового проекта"
        query = table_projects.select(table_projects.c.p_name == New_project)
        res = await database.fetch_one(query)
        if not res is None:
            return {"error" : "Проект с таким названием уже существует"}
        else:
            P_ID = uuid4()
            query = table_projects.insert().values(
                    p_id = P_ID,
                    p_name = json.p_name,
                    p_description = json.p_description,
                    p_datacreate = datetime.now(),
                    u_id = author_id )
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                {"message" : "Создан новый проект",
                 "p_id" : P_ID }

    async def name(P_ID):
        "возвращаем имя проекта по id проекта"
        query = table_projects.select(table_projects.c.p_id == P_ID)
        res = await database.fetch_one(query)
        
        if  res is None:
            return None
        else:
            return res["p_name"]

   

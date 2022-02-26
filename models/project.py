from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from base import database, table_projects


class Project(BaseModel):
    p_id : UUID = Field(default_factory=uuid4)
    p_name : str
    p_description : str
    p_datacreate: datetime
    u_id : UUID = Field(default_factory=uuid4)

    async def create(author_id, p_name: str, p_description: str):
        "Процедура создания нового проекта"
        query = table_projects.select(table_projects.c.p_name == p_name)
        res = await database.fetch_one(query)
        if not res is None:
            return {"error" : "Проект с таким названием уже существует"}
        else:
            P_ID = uuid4()
            query = table_projects.insert().values(
                    p_id = P_ID,
                    p_name = p_name,
                    p_description = p_description,
                    p_datacreate = datetime.now(),
                    u_id = author_id )
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Создан новый проект",
                        "p_id" : P_ID }

    async def name(P_ID):
        "возвращаем имя проекта по id проекта"
        query = table_projects.select(table_projects.c.p_id == P_ID)
        res = await database.fetch_one(query)
        
        if  res is None:
            return None
        else:
            return res["p_name"]

    async def id(P_NAME):
        "возвращаем p_id проекта по имени проекта"
        query = table_projects.select(table_projects.c.p_name == P_NAME)
        res = await database.fetch_one(query)
        
        if  res is None:
            return None
        else:
            return res["p_id"]

    async def get_project(name: str):
        "возвращаем проект по его имени"
        query = table_projects.select(table_projects.c.p_name == name)
        res = await database.fetch_one(query)

        if res is None:
            return {"error" : "Нет такого проекта"}
        else:
            return res

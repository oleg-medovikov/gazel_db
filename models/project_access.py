from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from base import database, table_project_access

class New_project_access(BaseModel):
    token : str
    p_id  : str
    u_id  : str
    access_level : int

class Project_access(BaseModel):
    p_id : UUID = Field(default_factory=uuid4)
    u_id : UUID = Field(default_factory=uuid4)
    access_level : int

    async def add_access(json : New_project_access):
        """Процедура добавления новых прав
        сначала нужно проверить, что такая строка уже не существует"""
        query = table_project_access.select(
                table_project_access.c.p_id == json.p_id,
                table_project_access.c.u_id == json.u_id)
        res = await database.fetch_one(query)

        if res is None:
            query = table_project_access.insert().values(
                    p_id = json.p_id,
                    u_id = json.u_id,
                    access_level = json.access_level)
            try:
                await database.execute(query)
            except Exception:
                return {"error" : str(Exception)}
            else:
                return {"message" : "Права добавлены"}
        else:
            return {"error" : "Права уже существуют"}
    
    async def update(json : New_project_access):
        "Обновление уровня прав"
        query = table_project_access.select(
                table_project_access.c.p_id == json.p_id,
                table_project_access.c.u_id == json.u_id)
        res = await database.fetch_one(query)

        if not res is None: 
            query = table_project_access.update()\
                    .where(table_project_access.c.p_id == json.p_id,
                           table_project_access.c.u_id == json.u_id)\
                    .values(access_level = json.access_level)
            try:
                await database.execute(query)
            except Exception:
                return {"error" : str(Exception)}
            else:
                return {"message" : "Обновил уровень прав"}
        else:
            return {"error" : "Таких прав не сущетсвует"}

    async def list_projects(U_ID):
        query = table_project_access.select(
                table_project_access.c.u_id == U_ID)
        
        res = await database.fetch_all(query) 

        list_ = []
        for row in res:
            list_append(row['p_id'])

        return list_


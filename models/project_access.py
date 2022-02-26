from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field
from sqlalchemy import and_

from base import database, table_project_access


class Project_access(BaseModel):
    p_id : UUID = Field(default_factory=uuid4)
    u_id : UUID = Field(default_factory=uuid4)
    access_level : int

    async def add_access(P_ID, U_ID, ACCESS_LEVEL):
        """Процедура добавления новых прав
        сначала нужно проверить, что такая строка уже не существует"""
        query = table_project_access.select().where(and_(
                table_project_access.c.p_id == P_ID,
                table_project_access.c.u_id == U_ID))

        res = await database.fetch_one(query)

        if res is None:
            query = table_project_access.insert().values(
                    p_id = P_ID,
                    u_id = U_ID,
                    access_level = ACCESS_LEVEL)
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Права добавлены"}
        else:
            return {"error" : "Права уже существуют"}
    
    async def remove_access(P_ID,U_ID):
        "Удаление прав пользователя"
        query = table_project_access.delete().where(and_(
                table_project_access.c.p_id == P_ID,
                table_project_access.c.u_id == U_ID))
        
        try:
            res = await database.execute(query)
        except Exception as e:
            return {"error" : str(e)}
        else:
            return {"message" : "права пользователя успешно удалены"}

    async def update(P_ID, U_ID, ACCESS_LEVEL):
        "Обновление уровня прав"
        query = table_project_access.select(
                table_project_access.c.p_id == P_ID,
                table_project_access.c.u_id == U_ID)
        res = await database.fetch_one(query)

        if not res is None: 
            query = table_project_access.update()\
                    .where(table_project_access.c.p_id == P_ID,
                           table_project_access.c.u_id == U_ID)\
                    .values(access_level = ACCESS_LEVEL)
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Обновил уровень прав"}
        else:
            return {"error" : "Таких прав не сущетсвует"}

    async def list_projects(U_ID):
        "возвращает список проектов для пользователя"
        query = table_project_access.select(
                table_project_access.c.u_id == U_ID)
        res = await database.fetch_all(query) 

        list_ = []
        for row in res:
            list_.append(row['p_id'])

        return list_

    async def list_users(P_ID):
        "Пользователи причастные к проекту"
        query = table_project_access.select(
                table_project_access.c.p_id == P_ID)
        return await database.fetch_all(query)
        

from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field
from sqlalchemy import select

from base import database, table_projects_reference


class Reference(BaseModel):
    r_id: UUID = Field(default_factory=uuid4)
    p_id: UUID = Field(default_factory=uuid4)
    d_id: UUID = Field(default_factory=uuid4)
    r_name : str
    r_code_name_level_1 : str
    r_code_name_level_2 : int
    r_code_name_level_3 : int
    r_date_create : datetime
    r_last_update : datetime

    async def create(
            P_ID, R_NAME,
            R_CODE_NAME_LEVEL_1,
            R_CODE_NAME_LEVEL_2,
            R_CODE_NAME_LEVEL_3
            ):
        "Создаём наименование, сперва проверка на наличие"

        query = table_projects_reference.select().where(and_(
            table_projects_reference.c.p_id == P_ID,
            table_projects_reference.c.r_code_name_level_1 == R_CODE_NAME_LEVEL_1,
            table_projects_reference.c.r_code_name_level_2 == R_CODE_NAME_LEVEL_2,
            table_projects_reference.c.r_code_name_level_3 == R_CODE_NAME_LEVEL_3
            ))

        res = await database.fetch_one(query)
        
        if not res is None:
            return {"error" : "Такое наименование уже существует"}
        else:
            NOW = datetime.now()
            query = table_projects_reference.insert().values(
                    r_id = uuid4(),
                    p_id = P_ID,
                    r_name = R_NAME,
                    r_code_name_level_1 = R_CODE_NAME_LEVEL_1,
                    r_code_name_level_2 = R_CODE_NAME_LEVEL_2,
                    r_code_name_level_3 = R_CODE_NAME_LEVEL_3,
                    r_date_create = NOW,
                    r_last_update = NOW
                    )
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"message" : "Наименование успешно добавлено"}

    async def level1(P_ID):
        "Получаем список нуменклатур проекта первого уровня"
        
        query = table_projects_reference.select().where(
                table_projects_reference.c.p_id == P_ID
                )
    
        res = await database.fetch_all(query)

        if not res is None: 
            list_ = []
            for row in res:
                list_.appaend(row['r_code_name_level_1'])
            list_.sort()
            
            return list_
        else:
            return []

    async def level2(P_ID, R_CODE_NAME_LEVEL_1):
        "Получаем список нуменклатур проекта второго уровня"
        
        query = table_projects_reference.select().where(and_(
                table_projects_reference.c.p_id == P_ID,
                table_projects_reference.c.r_code_name_level_1 == R_CODE_NAME_LEVEL_1
                ))
    
        res = await database.fetch_all(query)

        if not res is None: 
            list_ = []
            for row in res:
                list_.appaend(row['r_code_name_level_2'])
            list_.sort()
            
            return list_
        else:
            return []

    async def level3(P_ID,
            R_CODE_NAME_LEVEL_1,
            R_CODE_NAME_LEVEL_2):
        "Получаем список нуменклатур проекта третьего уровня"
        
        query = table_projects_reference.select().where(and_(
                table_projects_reference.c.p_id == P_ID,
                table_projects_reference.c.r_code_name_level_1 == R_CODE_NAME_LEVEL_1,
                table_projects_reference.c.r_code_name_level_2 == R_CODE_NAME_LEVEL_2
                ))
    
        res = await database.fetch_all(query)

        if not res is None: 
            list_ = []
            for row in res:
                list_.appaend(row['r_code_name_level_3'])
            list_.sort()
            
            return list_
        else:
            return []

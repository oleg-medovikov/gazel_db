from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy import and_
from pydantic import BaseModel, Field

from base import database, table_objects

class Object(BaseModel):
    r_id : UUID = Field(default_factory=uuid4)
    o_id : UUID = Field(default_factory=uuid4)
    u_id : UUID = Field(default_factory=uuid4)
    o_file_name : str
    o_date_create : datetime
    o_version : str
    o_hash_sum : str
    o_hidden : bool

    async def create(R_ID,U_ID,O_FILE_NAME,O_HASH_SUM):
        "Процедура добавления объекта"
        query = table_objects.select().where(and_(
            table_objects.c.r_id == R_ID,
            table_objects.c.o_hash_sum == O_HASH_SUM
            ))

        res = await database.fetch_one(query)
        if not res is None:
            return {"error" : "Такой объект уже существует"}
        else:
            O_ID = uuid4()
            query = table_objects.insert().values(
                    r_id = R_ID,
                    o_id = O_ID,
                    u_id = U_ID,
                    o_file_name = O_FILE_NAME,
                    o_date_create = datetime.now(),
                    o_version = 'incredible',
                    o_hash_sum = O_HASH_SUM,
                    o_hidden = False
                    )
            try:
                await database.execute(query)
            except Exception as e:
                return {"error" : str(e)}
            else:
                return {"O_ID" : O_ID}

    async def update_hash(O_ID, O_HASH_SUM):
        "Обновляем хеш сумму у файла"
        query = table_objects.update() \
                .where(table_objects.c.o_id == O_ID) \
                .values(o_hash_sum = O_HASH_SUM)
        try:
            await database.execute(query)
        except Exception as e:
            return {"error" : str(e)}
        else: 
            return {"message" : "Хеш файла обновлен"}

    async def files(R_ID):
        "Возвращает список файлов для данного обозначения"
        
        query = table_objects.select().where(
                table_objects.c.r_id == R_ID
                )

        return await database.fetch_all(query)
        

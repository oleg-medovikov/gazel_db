from uuid import uuid4, UUID
from sqlalchemy import and_
from pydantic import BaseModel, Field
import base64

from base import database, table_objects_binary


class Object_binary(BaseModel):
    o_id : UUID = Field(default_factory=uuid4)
    o_binary : bytes
 
    async def create(O_ID, O_BINARY):
        "Процедура загрузки файла в базу"
        query = table_objects_binary.select(table_objects_binary.c.o_id == O_ID)
        res = await database.fetch_one(query)
        
        if not res is None:
            return {"error" : "Такой бинарник уже существует"}
        else:
            query = table_objects_binary.insert().values(
                    o_id = O_ID,
                    o_binary =  base64.b64encode(O_BINARY.read()), 
                    )

            try:
                await database.execute(query)
            except Exception as e:
                print(str(e))
                return {"error" : str(e)}
            else:
                return {"message" : "Файл успешно загружен"}

    async def update(O_ID, O_BINARY):
        "обновить файл в базе"
        query = table_objects_binary.select(table_objects_binary.c.o_id == O_ID)
        res = await database.fetch_one(query)
        
        if res is None:
            return {"error" : "Такого бинарника не существует"}
        
        query = table_objects_binary.update() \
                .where(table_objects_binary.c.o_id == O_ID) \
                .values(o_binary = base64.b64encode(O_BINARY.read()) )

        try:
            await database.execute(query)
        except Exception as e:
            return {"error" : str(e)}
        else:
            return {"message" : "Файл успешно обновлён"}

    async def read(O_ID):
        "Прочитать файл из базы"
        query = table_objects_binary.select(table_objects_binary.c.o_id == O_ID)
        res = await database.fetch_one(query)
        
        if res is None:
            return {"error" : "Такой объекта не существует"}
        else:
            return res 

    async def delete(O_ID):
        "Удалить файл из базы"
        query = table_objects_binary.select(table_objects_binary.c.o_id == O_ID)
        res = await database.fetch_one(query)
        
        if res is None:
            return {"error" : "Такой объект не существует"}

        query = table_objects_binary.delete(table_objects_binary.c.o_id == O_ID)

        try:
            await database.execute(query)
        except Exception as e:
            return {"error" : str(e)}
        else:
            return {"message" : "Файл удалён"}

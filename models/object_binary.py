from uuid import uuid4, UUID
from sqlalchemy import and_
from pydantic import BaseModel, Field

from base import database, table_objects_binary


class Object_binary(BaseModel):
    o_id : UUID = Field(default_factory=uuid4)
    o_binary : bytes
 
    async def create(O_ID, O_BINARY):
        "Процедура загрузки файла в базу"
        query = table_objects_binary.select(table_objects_binary.c.o_id == O_ID)
        res = await database.fetch_one(query)
        
        if not res is None:
            return {"error" : "Такой объект уже существует"}
        else:
            query = table_objects_binary.insert().values(
                    o_id = O_ID,
                    o_binary =  O_BINARY
                    )

            try:
                await database.execute(query)
            except Exception as e:
                print(str(e))
                return {"error" : str(e)}
            else:
                return {"message" : "Ok"}

    async def read(O_ID):
        "Прочитать файл из базы"
        query = table_objects_binary.select(table_objects_binary.c.o_id == O_ID)
        res = await database.fetch_one(query)
        
        if not res is None:
            return {"error" : "Такой объект уже существует"}
        else:
            return {"file" : res['o_binary']} 

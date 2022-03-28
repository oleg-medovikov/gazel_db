from pydantic import BaseModel
from pathlib import Path
import shutil, os

from base import database, table_objects
from configuration import DATA_FILES

from fastapi.responses import FileResponse


class Object_file(BaseModel):
#    path : Path()
    
    async def write( O_ID, FILE):
        "Запись нового файла"
        query = table_objects.select(table_objects.c.o_id == O_ID)

        res = await database.fetch_one(query)

        if res is None:
            return {"error" : "Нет объекта для этого файла"}
        else:
            destination = DATA_FILES / res['r_id'].hex 
            if not destination.is_dir():
                os.makedirs(destination)

            destination = destination/ res["o_file_name"]
            try:
                with open(destination, "wb") as buffer:
                    shutil.copyfileobj(FILE.file, buffer)
            except Exception as e:
                return {"error" : str(e)}
            finally:
                #FILE.file.close()
                return {"message"  : "Файл сохранен"}

    async def delete( O_ID ):
        "Удаление файла"
        query = table_objects.select(table_objects.c.o_id == O_ID)

        res = await database.fetch_one(query)

        if res is None:
            return {"error" : "Нет объекта для этого файла"}
        else:
            query = table_objects.delete().where(
                    table_objects.c.o_id == O_ID
                    )

            await database.execute(query) 

            destination = DATA_FILES / res["r_id"].hex / res["o_file_name"]

            try:
                destination.unlink()
            except Exception as e:
                return {"error" : str(e)}
            finally:
                if not destination.is_file():
                    return {"message"  : "Файл удалён"}
                else:
                    return {"error" : "Файл не удалился"}

    async def read( O_ID ):
        "Чтение файла"
        query = table_objects.select(table_objects.c.o_id == O_ID)

        res = await database.fetch_one(query)

        if res is None:
            return {"error" : "Нет объекта для этого файла"}
        else:
            destination = DATA_FILES / res["r_id"].hex / res["o_file_name"]

            if not destination.is_file():
                return {"error" : "Файл не найден"}
            else:
                return FileResponse(
                        path=destination,
                        filename=res["o_file_name"])                 


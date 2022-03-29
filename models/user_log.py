from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field
from sqlalchemy import or_

from base import database, table_users_log

class User_log(BaseModel):
    p_id: UUID = Field(default_factory=uuid4)
    r_id: UUID = Field(default_factory=uuid4)
    u_id: UUID = Field(default_factory=uuid4)
    l_time : datetime
    event : str

    async def create(P_ID, R_ID, U_ID, EVENT):
        "Процедура добавления строчки лога"
        query = table_users_log.insert().values(
                p_id = P_ID,
                r_id = R_ID,
                u_id = U_ID,
                l_time = datetime.now(),
                event = EVENT
                )

        return await database.execute(query)

    async def list_events(ID):
        "Процедура чтения лога по проекту референсу или юзеру"
        query = table_users_log.select().values(or_(
            table_users_log.c.p_id == ID,
            table_users_log.c.r_id == ID,
            table_users_log.c.u_id == ID
            ))

        return await database.fetch_all(query)

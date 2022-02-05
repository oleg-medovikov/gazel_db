from .base import metadata

from sqlalchemy import Table, Column, String
from sqlalchemy.dialects.postgresql import UUID
import datetime

table_users_log = Table(
    "users_log",
    metadata,
    Column('u_id', UUID()), # идентификатор юзера
    Column('r_id', UUID()), # идентификатор референса 
    Column('l_time', datetime.datetime), # дата события 
    Column('event', String), # событие 
        )

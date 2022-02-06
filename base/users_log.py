from .base import metadata

from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

table_users_log = Table(
    "users_log",
    metadata,
    Column('u_id', UUID()), # идентификатор юзера
    Column('r_id', UUID()), # идентификатор референса 
    Column('l_time', DateTime), # дата события 
    Column('event', String), # событие 
        )

import datetime

from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

table_projects = Table(
    "projects",
    metadata,
    Column('p_id', UUID(), primary_key=True, default=uuid.uuid4), #уникальный идентификатор проекта
    Column('p_name', String), # название проекта
    Column('p_description', String), # описание
    Column('p_datacreate', datetime.datetime), # Дата создания
    Column('u_id', UUID()), # автор проекта, его администратор
        )

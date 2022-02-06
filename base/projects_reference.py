from .base import metadata

from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

table_projects_reference = Table(
    "projects_reference",
    metadata,
    Column('r_id', UUID()), # идентификатор ссылки в проекте
    Column('p_id', UUID()), # идентификатор проекта к которому принадлежит ссылка
    Column('d_id', UUID()), # Идентификатор описания ссылки
    Column('r_name', String), # Понятное человеку имя ссылки
    Column('r_code_name_level_1', String),  #1 уровень номенклатурного индекса
    Column('r_code_name_level_2', Integer), #2 уровень номенклатурного индекса
    Column('r_code_name_level_3', Integer), #3 уровень номенклатурного индекса
    Column('r_date_create', DateTime), # время создания ссылки
    Column('r_last_update', DateTime), # время последнего редактирования ссылки
        )


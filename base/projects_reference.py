from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

import datetime

table_projects_reference = Table(
    "projects_reference",
    metadata,
    Columns('r_id', UUID()), # идентификатор ссылки в проекте
    Columns('p_id', UUID()), # идентификатор проекта к которому принадлежит ссылка
    Columns('d_id', UUID()), # Идентификатор описания ссылки
    Columns('r_name', String), # Понятное человеку имя ссылки
    Columns('r_code_name_level_1', String),  #1 уровень номенклатурного индекса
    Columns('r_code_name_level_2', Integer), #2 уровень номенклатурного индекса
    Columns('r_code_name_level_3', Integer), #3 уровень номенклатурного индекса
    Columns('r_date_create', datetime.datetime), # время создания ссылки
    Columns('r_last_update', datetime.datetime), # время последнего редактирования ссылки
        )


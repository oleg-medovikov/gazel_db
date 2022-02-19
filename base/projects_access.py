from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

table_project_access = Table(
    "project_access",
    metadata,
    Column('p_id', UUID()), #идентификатор проекта
    Column('u_id', UUID()), #идентификатор пользователя
    Column('access_level', Integer), #уровень доступа
        )

"""
    0 - полный доступ, можно удалять и редактировать файлы проекта
    1 - доступ к добавлению новых файлов
    2 - доступ только на загрузку файлов
    3 - доступ только для просмотра
"""



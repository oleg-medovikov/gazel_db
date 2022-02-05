from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

table_projects_reference_description = Table(
    "projects_reference_description",
    metadata,
    Column('d_id', UUID()), # идентификатор описания ссылки
    Column('d_number', Integer), # порядковый номер тега
    Column('d_tag_name', String), # Имя тега описания ссылки
    Column('d_tag_value', String), # значение тега
    Column('d_tag_hidden', Boolean), # является ли тег скрытым
        )


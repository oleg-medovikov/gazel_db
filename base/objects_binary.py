from .base import metadata

from sqlalchemy import Table, Column, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

table_objects_binary = Table(
    "objects_binary",
    metadata,
    Column('o_id', UUID()), # идентификатор файла
    Column('o_binary', LargeBinary), # бинарное представление файла
        )

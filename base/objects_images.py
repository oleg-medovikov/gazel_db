from .base import metadata

from sqlalchemy import Table, Column, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID

table_objects_images = Table(
    "objects_images",
    metadata,
    Column('o_id', UUID()), # идентификатор файла
    Column('i_description', String), # подпись под рисунком
    Column('i_image', LargeBinary), # бинарное представление файла
        )

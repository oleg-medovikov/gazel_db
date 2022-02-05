from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

table_objects = Table(
    "objects",
    metadata,
    Column('r_id', UUID()), # идентификатор референса
    Column('o_id', UUID()), # индентификатор объекта (файла)
    Column('u_id', UUID()), # индентификатор автора объекта (файла)
    Column('o_file_name', String), # название файла
    Column('o_date_create', datetime.datetime), # время загрузки файла
    Column('o_version', String), # Версия файла, если нужно будет
    Column('o_hash_sum', String), # md5 хэш сумма файла
    Column('o_hidden', Boolean), # является ли файл скрытым
        )

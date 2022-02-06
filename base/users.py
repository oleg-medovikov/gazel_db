from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid


table_users = Table(
    "users",
    metadata,
    Column('u_id', UUID(), primary_key=True, default=uuid.uuid4), #уникальный идентификатор пользователя
    Column('first_name', String), # Имя и отчество пользователя
    Column('second_name', String), # Фамилия пользователя
    Column('username', String), #логин пользователя
    Column('password_hash', String), # хеш пароля
    Column('position', String), # Рабочая должность
    Column('admin', Boolean), # является ли админом
    Column('token', String), # токен пользователя, на будущее 
        )

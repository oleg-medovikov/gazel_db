from starlette.config import Config
from .security import hash_password

config = Config(".env")

DATABASE_URL = config("DATABASE_URL",cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#===create admin =====
admin = {
        "first_name" : config("first_name", cast=str),
        "second_name" : config("second_name", cast=str),
        "username" : config("username", cast=str),
        "password_hash" : hash_password(config("password", cast=str)),
        "position" : config("position", cast=str),
        "admin" : True
        }


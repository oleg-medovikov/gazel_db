from starlette.config import Config
from passlib.hash import md5_crypt
from pathlib import Path
import os

config = Config(".env")

DATABASE_URL = config("DATABASE_URL",cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SALT = config("SALT", cast=str)

#===create admin =====
def hash_password(password: str) -> str:
    "Хеширование пароля"
    return md5_crypt.encrypt(password,salt=SALT)


admin = {
        "first_name" : config("first_name", cast=str),
        "second_name" : config("second_name", cast=str),
        "username" : config("username", cast=str),
        "password_hash" : hash_password(config("password", cast=str)),
        "position" : config("position", cast=str),
        "admin" : True,
        "token" : ''
        }
#=====================

DATA_FILES = Path(Path.home(), 'Gazel_fl')

if not DATA_FILES.is_dir():
    os.makedirs(DATA_FILES)

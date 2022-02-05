from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL",cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = 60



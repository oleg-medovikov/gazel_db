from .app import app

from models import User
from configuration import admin

@app.get("/")
async def main():
    "Для отладки, добавление админа"
    try:
        res = await User.add_user(New_user(**admin))
    except Exception:
        return {"error" : str(Exception)}
    else:
        return res



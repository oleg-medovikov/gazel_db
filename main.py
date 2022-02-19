import uvicorn 
from requests import app

if __name__ == "__main__":
    uvicorn.run("main:app",
            host="0.0.0.0",port=10000,
            reload=True,workers =2, 
            ssl_keyfile='public/oleg.key', 
            ssl_certfile='public/oleg.crt',)



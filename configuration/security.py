from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    "Хеширование пароля"
    return pwd_context.hash(password)

def verify_passwd(password: str, hash: str) -> bool:
    "Сравнение пароля с хешем"
    return pwd_context.verify(password,hash)



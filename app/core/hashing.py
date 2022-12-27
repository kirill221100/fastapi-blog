from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def hash_password(password: str):
    return pwd_cxt.hash(password)


async def verify(normal_password, hashed_password):
    return pwd_cxt.verify(normal_password, hashed_password)

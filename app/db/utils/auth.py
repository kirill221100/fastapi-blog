from fastapi import HTTPException
from app.db.db_setup import users_collection
from app.db.utils.user import get_user_by_username
from app.schemas.auth import RegisterSchema
from app.core.hashing import hash_password, verify
from app.core.jwt import create_token


async def register(schema: RegisterSchema):
    if not await get_user_by_username(schema.username):
        data = dict(schema)
        data['password'] = await hash_password(schema.password)
        data['avatar'] = ''
        data['about'] = ''
        await users_collection.insert_one(data)
        new_user = await get_user_by_username(schema.username)
        return create_token(new_user)
    raise HTTPException(status_code=400, detail=f"User with username '{schema.username}' already exists")


async def login(username, password):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail=f"User with username {username} doesn't exists")
    if not await verify(password, user['password']):
        raise HTTPException(status_code=401, detail=f"Incorrect password")
    return create_token(user)

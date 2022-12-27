from fastapi import HTTPException, UploadFile, status
from bson import ObjectId
from app.db.db_setup import users_collection
from app.broker.publisher import Publisher


def mongodb_user_response(user):
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'password': user['password'],
        'about': user['about'],
        'avatar': user['avatar']
    }


async def check_user(user_id: str):
    try:
        user_id = ObjectId(user_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail=f'Id {user_id} is invalid')
    user = await users_collection.find_one({'_id': user_id})
    if user:
        return mongodb_user_response(user)
    raise HTTPException(status_code=404, detail=f'User with id {user_id} is not found')


async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return mongodb_user_response(user)


async def get_user_for_changes(user_id: str):
    user = await users_collection.find_one({'_id': ObjectId(user_id)})
    return mongodb_user_response(user)


async def get_user_by_username(username: str):
    user = await users_collection.find_one({'username': username})
    if user:
        return mongodb_user_response(user)


async def change(username: str, about: str, avatar: UploadFile, user_id: str):
    user = await get_user_for_changes(user_id)
    if username:
        user['username'] = username
    if about:
        user['about'] = about
    if avatar:
        pub = await Publisher().connect()
        user['avatar'] = await pub.call(avatar.file.read())
    await users_collection.replace_one({'_id': ObjectId(user_id)}, user)
    return await get_user_by_id(user_id)


async def delete_profile(user_id: str):
    await users_collection.delete_one({'_id': ObjectId(user_id)})
    return status.HTTP_200_OK

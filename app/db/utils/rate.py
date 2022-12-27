from fastapi import status, HTTPException
from app.db.db_setup import rates_collection


async def drop_rate(user_id: str, post_id: str, r: str):
    if not await if_rate_exists(user_id, post_id, r):
        raise HTTPException(status_code=400)
    data = {'user_id': user_id, 'post_id': post_id, 'rate': r}
    res = await rates_collection.delete_one(data)
    return res


async def get_rate(user_id: str, post_id: str):
    data = {'user_id': user_id, 'post_id': post_id}
    res = await rates_collection.find_one(data)
    try:
        return res.get('rate')
    except AttributeError:
        return None


async def if_rate_exists(user_id: str, post_id: str, r: str):
    data = {'user_id': user_id, 'post_id': post_id, 'rate': r}
    return await rates_collection.find_one(data)


async def rate(user_id: str, post_id: str, r: str):
    data = {'user_id': user_id, 'post_id': post_id, 'rate': r}
    await rates_collection.insert_one(data)
    return status.HTTP_200_OK

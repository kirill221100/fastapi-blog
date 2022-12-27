import asyncio

from fastapi import HTTPException, status, UploadFile
from app.db.db_setup import posts_collection
from app.db.utils.user import check_user
from app.db.utils.rate import drop_rate, rate, get_rate
from app.schemas.post import PostSchema
from app.broker.publisher import Publisher
from bson import ObjectId, errors
from datetime import datetime, timedelta
from typing import Literal


def mongodb_post_response(post):
    return {
        'id': str(post['_id']),
        'text': post['text'],
        'user_id': post['user_id'],
        'date': post['date'],
        'likes': post['likes'],
        'dislikes': post['dislikes'],
        'pic': post['pic']
    }


async def get_posts(page: int = 0):
    result = []
    posts = posts_collection.find({}).skip(10 * page).limit(10)
    async for post in posts:
        result.append(mongodb_post_response(post))
    return result


async def get_post_by_id(post_id: str):
    try:
        post_id = ObjectId(post_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail=f'Id {post_id} is invalid')
    post = await posts_collection.find_one({'_id': post_id})
    if post:
        return mongodb_post_response(post)
    raise HTTPException(status_code=404, detail=f'Post with id {post_id} is not found')


async def get_users_posts(user_id: str):
    await check_user(user_id)
    result = []
    posts = posts_collection.find({'user_id': user_id})
    async for post in posts:
        result.append(mongodb_post_response(post))
    return result


async def get_post_for_changes(post_id: str):
    post = await get_post_by_id(post_id)
    post.pop('id')
    return post


async def rate_post(user_id: str, post_id: str, r: Literal['like', 'dislike']):
    post = await get_post_for_changes(post_id)
    check = await get_rate(user_id, post_id)
    if r == 'like' and check != 'like':
        post['likes'] += 1
        if check == 'dislike':
            await drop_rate(user_id, post_id, 'dislike')
            post['dislikes'] -= 1
    elif r == 'dislike' and check != 'dislike':
        post['dislikes'] += 1
        if check == 'like':
            await drop_rate(user_id, post_id, 'like')
            post['likes'] -= 1
    else:
        raise HTTPException(status_code=400, detail=f'Already {r}d this post')
    await posts_collection.replace_one({'_id': ObjectId(post_id)}, post)
    return await rate(user_id, post_id, r)


async def drop_like(user_id: str, post_id: str):
    await drop_rate(user_id, post_id, 'like')
    post = await get_post_for_changes(post_id)
    post['likes'] -= 1
    await posts_collection.replace_one({'_id': ObjectId(post_id)}, post)
    return status.HTTP_200_OK


async def drop_dislike(user_id: str, post_id: str):
    await drop_rate(user_id, post_id, 'dislike')
    post = await get_post_for_changes(post_id)
    post['dislikes'] -= 1
    await posts_collection.replace_one({'_id': ObjectId(post_id)}, post)
    return status.HTTP_200_OK


async def create_post(user_id: str, pic: UploadFile, text: str):
    pub = await Publisher().connect()
    data = {'text': text, 'user_id': user_id, 'date': datetime.now(), 'likes': 0, 'dislikes': 0,
            'pic': await pub.call(pic.file.read())}
    post = await posts_collection.insert_one(data)
    new_post = await posts_collection.find_one({'_id': post.inserted_id})
    return mongodb_post_response(new_post)


async def update_post(user_id: str, post_id: str, text: str, pic: UploadFile):
    if not any([text, pic]):
        raise HTTPException(status_code=400, detail="Empty arguments")
    post = await get_post_for_changes(post_id)
    if post['user_id'] != user_id:
        raise HTTPException(status_code=400, detail="You're not an author of this post")
    if post['date'] - datetime.now() > timedelta(hours=1):
        raise HTTPException(status_code=400, detail="You can't edit posts after an hour has passed")
    if text:
        post['text'] = text
    if pic:
        pub = await Publisher().connect()
        post['pic'] = await pub.call(pic.file.read())
    await posts_collection.replace_one({'_id': ObjectId(post_id)}, post)
    return await get_post_by_id(post_id)


async def delete_post(user_id: str, post_id: str):
    post = await get_post_by_id(post_id)
    if post['user_id'] != user_id:
        raise HTTPException(status_code=400, detail="You're not an author of this post")
    await posts_collection.delete_one({'_id': ObjectId(post_id)})
    return status.HTTP_200_OK

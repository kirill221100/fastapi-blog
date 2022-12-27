from fastapi import APIRouter, Depends, UploadFile, File
from app.db.utils.post import get_posts, create_post, get_post_by_id, update_post, delete_post, get_users_posts, \
    rate_post, drop_like, drop_dislike
from app.core.oauth import get_current_user_id
from app.schemas.post import PostSchema
from typing import Optional

post_router = APIRouter(prefix='/post')


@post_router.get('/all-posts')
async def all_posts(page: int = 0):
    return await get_posts(page)


@post_router.get('/get-by-id')
async def post_by_id(post_id: str):
    return await get_post_by_id(post_id)


@post_router.get('/get-users-posts')
async def get_usrs_posts(user_id: str):
    return await get_users_posts(user_id)


@post_router.post('/new-post')
async def new_post(text: str, pic: Optional[UploadFile] = File(None), user_id: str = Depends(get_current_user_id)):
    return await create_post(user_id, pic, text)


@post_router.put('/edit-post')
async def edit_post(post_id: str, text: Optional[str] = None, pic: Optional[UploadFile] = File(None),
                    user_id: str = Depends(get_current_user_id)):
    return await update_post(user_id, post_id, text, pic)


@post_router.delete('/delete-post-by-id')
async def delete_post_by_id(post_id: str, user_id: str = Depends(get_current_user_id)):
    return await delete_post(user_id, post_id)


@post_router.get('/like-post')
async def like_post(post_id: str, user_id: str = Depends(get_current_user_id)):
    return await rate_post(user_id, post_id, 'like')


@post_router.get('/dislike-post')
async def dislike_post(post_id: str, user_id: str = Depends(get_current_user_id)):
    return await rate_post(user_id, post_id, 'dislike')


@post_router.delete('/drop-like')
async def drop_li(post_id: str, user_id: str = Depends(get_current_user_id)):
    return await drop_like(user_id, post_id)


@post_router.delete('/drop-dislike')
async def drop_di(post_id: str, user_id: str = Depends(get_current_user_id)):
    return await drop_dislike(user_id, post_id)

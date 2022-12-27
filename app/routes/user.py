from fastapi import APIRouter, Depends, UploadFile, File
from app.core.oauth import get_current_user_id
from app.db.utils.user import get_user_by_id, change, delete_profile
from typing import Optional

user_router = APIRouter(prefix='/user')


@user_router.get('/me')
async def me(user_id: str = Depends(get_current_user_id)):
    return await get_user_by_id(user_id)


@user_router.put('/change-profile')
async def chng(username: Optional[str] = None, about: Optional[str] = None, avatar: Optional[UploadFile] = File(None),
               user_id: str = Depends(get_current_user_id)):
    return await change(username, about, avatar, user_id)


@user_router.delete('/delete-profile')
async def delete(user_id: str = Depends(get_current_user_id)):
    return await delete_profile(user_id)

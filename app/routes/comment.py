from fastapi import APIRouter, Depends
from app.schemas.comment import CommentSchema
from app.db.utils.comment import comment_post, get_posts_comments, delete_comment
from app.core.oauth import get_current_user_id

comment_router = APIRouter(prefix='/comment')


@comment_router.get('/get-comments-by-post-id')
async def get_comments_by_post_id(post_id: str):
    return await get_posts_comments(post_id)


@comment_router.post('/comment-post')
async def comment_the_post(comment: CommentSchema, user_id: str = Depends(get_current_user_id)):
    return await comment_post(user_id, comment)


@comment_router.delete('/delete-comment')
async def delete(comment_id: str, user_id: str = Depends(get_current_user_id)):
    return await delete_comment(user_id, comment_id)

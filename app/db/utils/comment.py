from fastapi import status, HTTPException
from app.db.utils.post import get_post_by_id
from app.db.db_setup import comments_collection
from app.schemas.comment import CommentSchema
from datetime import datetime
from bson import ObjectId


def mongodb_comment_response(comment):
    return {
        'id': str(comment['_id']),
        'text': comment['text'],
        'post_id': comment['post_id'],
        'user_id': comment['user_id'],
        'date': comment['date']
    }


async def get_comment_by_id(comment_id: str):
    comment = await comments_collection.find_one({'_id': ObjectId(comment_id)})
    if comment:
        return mongodb_comment_response(comment)
    raise HTTPException(status_code=404, detail=f"Comment with id {comment_id} is not found")


async def get_posts_comments(post_id: str):
    await get_post_by_id(post_id)
    results = []
    comments = comments_collection.find({'post_id': post_id})
    async for comment in comments:
        results.append(mongodb_comment_response(comment))
    return results


async def comment_post(user_id: str, comment: CommentSchema):
    await get_post_by_id(comment.post_id)
    data = dict(comment)
    data['user_id'] = user_id
    data['date'] = datetime.now()
    comment_db = await comments_collection.insert_one(data)
    new_comment = await comments_collection.find_one({'_id': comment_db.inserted_id})
    return mongodb_comment_response(new_comment)


async def delete_comment(user_id: str, comment_id: str):
    comment = await get_comment_by_id(comment_id)
    if comment['user_id'] == user_id:
        await comments_collection.delete_one({'_id': ObjectId(comment_id)})
        return status.HTTP_200_OK
    raise HTTPException(status_code=400, detail=f"You're not an author of comment with id {comment_id}")

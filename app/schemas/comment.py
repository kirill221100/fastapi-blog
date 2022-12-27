from pydantic import BaseModel, constr


class CommentSchema(BaseModel):
    post_id: str
    text: str

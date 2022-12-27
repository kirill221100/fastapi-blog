from pydantic import BaseModel, constr


class PostSchema(BaseModel):
    text: str

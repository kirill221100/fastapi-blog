from pydantic import BaseModel, validator


class RegisterSchema(BaseModel):
    username: str
    password: str

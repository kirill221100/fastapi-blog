from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas.auth import RegisterSchema
from app.db.utils.auth import register, login
from app.core.oauth import check_if_logged_in

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/register')
async def reg(schema: RegisterSchema, check=Depends(check_if_logged_in)):
    return {"access_token": await register(schema), "token_type": "bearer"}


@auth_router.post('/login')
async def log(schema: OAuth2PasswordRequestForm = Depends(), check=Depends(check_if_logged_in)):
    return {"access_token": await login(schema.username, schema.password), "token_type": "bearer"}

from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.core.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401)
    user_id = verify_token(token)
    return user_id


async def check_if_logged_in(user: str = Depends(oauth2_scheme)):
    if user:
        raise HTTPException(status_code=400, detail="You're already logged in")
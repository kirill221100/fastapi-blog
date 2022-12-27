from fastapi import HTTPException
from app.core.config import Config as cfg
from datetime import datetime, timedelta
from jose import JWTError, jwt


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        decoded_token = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
        user_id: str = decoded_token.get('id')
        if user_id:
            return user_id
        raise HTTPException(status_code=401, detail='Invalid token')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

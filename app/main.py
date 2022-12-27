from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.post import post_router
from app.routes.comment import comment_router
from app.broker.publisher import Publisher

app = FastAPI(title='Blog', docs_url='/docs')

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(auth_router, tags=['auth'])
app.include_router(user_router, tags=['user'])
app.include_router(post_router, tags=['post'])
app.include_router(comment_router, tags=['comment'])

if __name__ == '__main__':
    run('main:app', reload=True, timeout_keep_alive=0)

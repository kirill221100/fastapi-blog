from fastapi import FastAPI
from uvicorn import run
from picture_storage_app.routes.pics import router

app2 = FastAPI(title='Picture storage', docs_url='/docs')
app2.include_router(router)

if __name__ == '__main__':
    run('main2:app2', host='localhost', port=5555, reload=True)

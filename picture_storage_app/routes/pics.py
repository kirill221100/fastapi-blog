import os
import asyncio
from fastapi import APIRouter, Response

router = APIRouter()


def read_file(name: str):
    with open('./images/' + name, 'rb') as f:
        return f.read()


@router.get('/')
async def get_pic(pic: str):
    return Response(content=await asyncio.get_event_loop().run_in_executor(None, read_file, pic),
                    media_type="image/jpg")

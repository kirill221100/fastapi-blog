import uuid
import aiormq
import asyncio
from fastapi import UploadFile
from app.core.pic import pic_to_base64
from app.core.config import Config as cfg
from typing import MutableMapping


class Publisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.callback_queue = ''
        self.futures = {}
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        self.connection = await aiormq.connect(cfg.AMQP_URL)
        self.channel = await self.connection.channel()
        declare_ok = await self.channel.queue_declare(
            exclusive=True, auto_delete=True, durable=True)
        await self.channel.basic_consume(declare_ok.queue, self.on_response)
        self.callback_queue = declare_ok.queue
        return self

    async def on_response(self, message: aiormq.abc.DeliveredMessage):
        future = self.futures.pop(message.header.properties.correlation_id)
        future.set_result(message.body)

    async def call(self, pic: bytes):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()
        self.futures[correlation_id] = future
        await self.channel.basic_publish(
            pic, timeout=1,
            routing_key=cfg.QUEUE_NAME,
            properties=aiormq.spec.Basic.Properties(
                content_type='text/plain',
                correlation_id=correlation_id,
                reply_to=self.callback_queue,
            )
        )
        return (await future).decode()

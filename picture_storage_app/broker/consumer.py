import random
import string
import os
from fastapi import UploadFile
import aiormq
import asyncio


def random_name():
    return ''.join([random.choice(string.ascii_letters) for _ in range(10)]) + '.jpg'


def load_pic(pic: bytes):
    files = os.listdir('./')
    while True:
        name = random_name()
        if name not in files:
            break
    with open('../images/' + name, mode='wb+') as f:
        f.write(pic)
    return name


async def on_message(message: aiormq.abc.DeliveredMessage):
    name = await asyncio.get_event_loop().run_in_executor(None, load_pic, message.body)

    await message.channel.basic_publish(
        name.encode(), routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id
        ),

    )

    await message.channel.basic_ack(message.delivery.delivery_tag)


async def main():
    connection = await aiormq.connect("amqp://guest:guest@127.0.0.1/")
    channel = await connection.channel()
    declare_ok = await channel.queue_declare('picture_queue')
    await channel.basic_consume(declare_ok.queue, on_message)

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

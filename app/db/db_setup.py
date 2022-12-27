import motor.motor_asyncio
from app.core.config import Config as cfg

client = motor.motor_asyncio.AsyncIOMotorClient(cfg.MONGO_DETAILS)

db = client.db
posts_collection = db.posts_collection
users_collection = db.users_collection
comments_collection = db.comments_collection
rates_collection = db.rates_collection

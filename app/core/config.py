class Config:
    MONGO_DETAILS = 'mongodb://localhost:27017'
    SECRET_KEY = 'secret'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    QUEUE_NAME = 'picture_queue'
    AMQP_URL = "amqp://guest:guest@127.0.0.1/"

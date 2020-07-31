# FastAPI
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Kafka
from kafka import KafkaProducer

# logger
from app.logger import logger

# config
from app.config import KAFKA_HOST, KAFKA_PORT

# route
from app.routers import object

# initialize FastAPI
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*']) # TODO: change allow_origins

# Kafka Producer client
kafka_producer = None


@app.on_event('startup')
def startup_event():
    global kafka_producer
    kafka_producer = KafkaProducer(
        bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT))

app.include_router(object.router, prefix="/_api/object", tags=["object"])

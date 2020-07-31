# FastAPI
from fastapi import FastAPI, APIRouter, File, Form, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Kafka
from kafka import KafkaProducer
from json import dumps

# logger
from app.logger import logger

# config
from app.config import KAFKA_HOST, KAFKA_PORT, S3_BUCKET_OBJECT, KAFKA_TOPIC_OBJECT_IMAGE

# S3
from app.s3 import upload_fileobj

# Kafka Producer client
kafka_producer = KafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}")

# initialize FastAPI
app = FastAPI()

# TODO: change allow_origins
app.add_middleware(CORSMiddleware, allow_origins=['*'])


@app.post("/", response_class=Response)
def object_image_input(image: UploadFile = File(...),  # ... = required
                       image_name: str = Form(...),
                       time: int = Form(...)):  # epoch (seconds)

    # Upload image to S3
    upload_fileobj(image.file, image_name, S3_BUCKET_OBJECT)
    image_s3_uri = f"s3://{S3_BUCKET_OBJECT}/{image_name}"
    logger.info(f"Image is uploaded to {image_s3_uri}")

    # Send data to Kafka
    message = {'image_path': image_s3_uri}
    kafka_producer.send(KAFKA_TOPIC_OBJECT_IMAGE,
                        value=dumps(message).encode(encoding='UTF-8'))
    logger.info(f"Message is published to Kafka: {dumps(message)}")

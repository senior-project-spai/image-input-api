# FastAPI
from fastapi import FastAPI, File, Form, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

# S3
import boto3
from botocore import UNSIGNED
from botocore.client import Config

# Kafka
from kafka import KafkaProducer
from json import dumps

# logger
from logger import logger

# config
from config import KAFKA_HOST, KAFKA_PORT, S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET_OBJECT, KAFKA_TOPIC_OBJECT_IMAGE

# initialize FastAPI
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])

kafka_producer = None


@app.on_event('startup')
def startup_event():
    global kafka_producer
    kafka_producer = KafkaProducer(
        bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT))


@app.post("/_api/object", response_class=Response)
def object_image_input(image: UploadFile = File(...),  # ... = required
                       image_name: str = Form(...),
                       time: int = Form(...)):  # epoch (seconds)

    # Upload image to S3
    s3_resource = boto3.resource('s3',
                                 endpoint_url=S3_ENDPOINT,
                                 aws_access_key_id=S3_ACCESS_KEY,
                                 aws_secret_access_key=S3_SECRET_KEY,
                                 config=Config(signature_version='s3v4'))
    bucket_name = S3_BUCKET_OBJECT
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_fileobj(image.file, image_name)
    image_s3_uri = "s3://{0}/{1}".format(bucket_name, image_name)
    logger.info("Image is uploaded to {}".format(image_s3_uri))

    # Send data to Kafka
    message = {'image_path': image_s3_uri}
    kafka_producer.send(KAFKA_TOPIC_OBJECT_IMAGE,
                        value=dumps(message).encode(encoding='UTF-8'))

# FastAPI
from fastapi import APIRouter, File, Form, UploadFile
from starlette.responses import Response

from json import dumps

from app.main import kafka_producer
from app.config import S3_BUCKET_OBJECT, KAFKA_TOPIC_OBJECT_IMAGE
from app.logger import logger
from app.s3 import upload_fileobj

router = APIRouter()


@router.post("/", response_class=Response)
def object_image_input(image: UploadFile = File(...),  # ... = required
                       image_name: str = Form(...),
                       time: int = Form(...)):  # epoch (seconds)

    # Upload image to S3
    upload_fileobj(image.file, image_name, S3_BUCKET_OBJECT)
    image_s3_uri = "s3://{0}/{1}".format(S3_BUCKET_OBJECT, image_name)
    logger.info("Image is uploaded to {}".format(image_s3_uri))

    # Send data to Kafka
    message = {'image_path': image_s3_uri}
    kafka_producer.send(KAFKA_TOPIC_OBJECT_IMAGE,
                        value=dumps(message).encode(encoding='UTF-8'))
    logger.info(f"Message is published to Kafka: {dumps(message)}",)

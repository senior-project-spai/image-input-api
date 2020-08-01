from fastapi import APIRouter, Response, UploadFile, File, Form
from json import dumps

from app import main, config
from app.s3 import upload_fileobj
from app.logger import logger

router = APIRouter()

@router.post("/", response_class=Response)
def object_image_input(image: UploadFile = File(...),  # ... = required
                       image_name: str = Form(...),
                       time: int = Form(...)):  # epoch (seconds)

    # Upload image to S3
    upload_fileobj(image.file, image_name, config.S3_BUCKET_OBJECT_IMAGE)
    image_s3_uri = f"s3://{config.S3_BUCKET_OBJECT_IMAGE}/{image_name}"
    logger.info(f"Image is uploaded to {image_s3_uri}")

    # Send data to Kafka
    message = {'image_path': image_s3_uri}
    main.kafka_producer.send(config.KAFKA_TOPIC_OBJECT_IMAGE,
                        value=dumps(message).encode(encoding='UTF-8'))
    logger.info(f"Message is published to Kafka: {dumps(message)}")
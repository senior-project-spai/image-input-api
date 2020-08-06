# ---------------------------------------------
# This route is for "FADE Integration"
# ---------------------------------------------

from fastapi import APIRouter, Response, UploadFile, File, Form, HTTPException
from json import dumps
import uuid
import pymysql
import time

from app.s3 import upload_fileobj
from app.logger import logger
from app import main, config

router = APIRouter()


@router.post("/", response_class=Response)
def object_image_input(image: UploadFile = File(...),  # ... = required
                       image_id: str = Form(None)): # Optional

    # Create connection to database
    sql_connection = pymysql.connect(**(config.MYSQL_CONFIG_FADE))

    # Manage image ID
    if image_id is None:
        image_id = uuid.uuid4().hex
    else:
        # Check that image_id is not exist in DB
        with sql_connection.cursor() as cursor:

            # Execute SQL query
            cursor.execute("SELECT EXISTS (SELECT id FROM image WHERE id=%(image_id)s);", {
                           'image_id': image_id})

            # Get result
            is_exist = bool(cursor.fetchone()[0])

        # Raise error if this image_id is exist
        if is_exist:
            sql_connection.close()  # Close sql connection first
            raise HTTPException(400, "image_id is exist in database")

    # Image path to S3
    image_s3_uri = f"s3://{config.S3_BUCKET_IMAGE}/{image_id}"

    # Insert into image table
    with sql_connection.cursor() as cursor:
        cursor.execute("INSERT INTO `image` (`id`, `path`, `timestamp`) VALUES (%(image_id)s, %(image_path)s, %(timestamp)s);", {
            'image_id': image_id,
            'image_path': image_s3_uri,
            # Epoch in milliseconds
            'timestamp': int(round(time.time() * 1000))
        })

    # Upload image to S3
    upload_fileobj(image.file, image_id, config.S3_BUCKET_IMAGE)
    logger.info(f"Image is uploaded to {image_s3_uri}")

    # Commit to database
    sql_connection.commit()
    sql_connection.close()

    # Send data to Kafka
    message = {'image_id': image_id, 'image_path': image_s3_uri}
    main.kafka_producer.send(config.KAFKA_TOPIC_IMAGE,
                             value=dumps(message).encode(encoding='UTF-8'))
    logger.info(f"Message is published to Kafka: {dumps(message)}")

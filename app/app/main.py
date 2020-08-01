# FastAPI
from fastapi import FastAPI, APIRouter, File, Form, UploadFile, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from pydantic import BaseModel
# Kafka
from json import dumps
# SQL
import pymysql
# import time
import time as time1

# logger
from app.logger import logger
# S3
from app.s3 import upload_fileobj
# kafka
from app.kafka import kafka_producer
# router
from app.routes import object
# config
from app.config import S3_BUCKET_FACE_IMAGE, KAFKA_TOPIC_FACE_IMAGE, MYSQL_CONFIG

# Initialize FastAPI
app = FastAPI()

# TODO: change allow_origins
app.add_middleware(CORSMiddleware, allow_origins=['*'])

app.include_router(object.router, prefix="/_api/object", tags=["object"])


class FaceImageInputResponseModel(BaseModel):
    face_image_id: int


@app.post("/_api/face", response_model=FaceImageInputResponseModel)
def face_image_input(background_tasks: BackgroundTasks,
                     image: UploadFile = File(...),  # ... = required
                     image_name: str = Form(...),
                     branch_id: int = Form(...),
                     camera_id: int = Form(...),
                     time: float = Form(...),
                     position_top: int = Form(None),  # None = not required
                     position_right: int = Form(None),
                     position_bottom: int = Form(None),
                     position_left: int = Form(None),
                     ):
    req_arrive_time = time1.time()

    # Insert data to SQL
    sql_connection = pymysql.connect(**MYSQL_CONFIG)
    image_id = None

    bucket_name = S3_BUCKET_FACE_IMAGE
    image_s3_uri = "s3://{0}/{1}".format(bucket_name, image_name)

    sql_start_time = time1.time()

    with sql_connection.cursor() as cursor:
        insert_sql = ("INSERT INTO `FaceImage` (`image_path`, `camera_id`, `branch_id`, `image_time`, `position_top`, `position_right`, `position_bottom`, `position_left`, `time`) "
                      "VALUES (%(image_path)s, %(camera_id)s, %(branch_id)s, %(image_time)s, %(position_top)s, %(position_right)s, %(position_bottom)s, %(position_left)s, %(time)s)")
        cursor.execute(insert_sql, {'image_path': image_s3_uri,
                                    'camera_id': camera_id,
                                    'branch_id': branch_id,
                                    'image_time': time,
                                    'position_top': position_top,
                                    'position_right': position_right,
                                    'position_bottom': position_bottom,
                                    'position_left': position_left,
                                    'time': int(round(time1.time() * 1000))/1000})
        sql_connection.commit()  # commit changes
        image_id = cursor.lastrowid  # get last inserted row id
    sql_connection.close()

    finish_sql_time = time1.time()

    obj = {'face_image_id': image_id,
           'face_image_path': image_s3_uri,
           'position_top': position_top,
           'position_right': position_right,
           'position_bottom': position_bottom,
           'position_left': position_left}

    background_tasks.add_task(
        upload_fileobj, image.file, image_name, bucket_name)
    background_tasks.add_task(add_message_to_kafka_face, obj)

    return_time = time1.time()
    print(req_arrive_time, sql_start_time, finish_sql_time, return_time)
    # Return ID to response
    return {'face_image_id': image_id}


def add_message_to_kafka_face(obj):
    kafka_producer.send(KAFKA_TOPIC_FACE_IMAGE,
                        value=dumps(obj).encode(encoding='UTF-8'))

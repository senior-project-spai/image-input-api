# FastAPI
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.logger import logger
from app.s3 import upload_fileobj
from app.kafka import kafka_producer
from app.routes import object, face, image

# Initialize FastAPI
app = FastAPI()

# CORS
# TODO: change allow_origins
app.add_middleware(CORSMiddleware, allow_origins=['*'])

# Routes
app.include_router(object.router, prefix="/_api/object", tags=["object"])
app.include_router(face.router, prefix="/_api/face", tags=["face"])
app.include_router(image.router, prefix="/_api/image", tags=['image'])

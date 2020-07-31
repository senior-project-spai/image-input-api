import os  # environment variable

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
KAFKA_TOPIC_OBJECT_IMAGE = os.getenv('KAFKA_TOPIC_OBJECT_IMAGE')

S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_BUCKET_OBJECT = os.getenv('S3_BUCKET_OBJECT')


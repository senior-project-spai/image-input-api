import os  # environment variable

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
KAFKA_TOPIC_OBJECT_IMAGE = os.getenv('KAFKA_TOPIC_OBJECT_IMAGE')
KAFKA_TOPIC_FACE_IMAGE = os.getenv('KAFKA_TOPIC_FACE_IMAGE')
KAFKA_TOPIC_IMAGE = os.getenv('KAFKA_TOPIC_IMAGE')

S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_BUCKET_OBJECT_IMAGE = os.getenv('S3_BUCKET_OBJECT_IMAGE')
S3_BUCKET_FACE_IMAGE = os.getenv('S3_BUCKET_FACE_IMAGE')
S3_BUCKET_IMAGE = os.getenv('S3_BUCKET_IMAGE')

MYSQL_CONFIG = {
    "host": os.getenv('MYSQL_MASTER_HOST'),
    "port": int(os.getenv('MYSQL_MASTER_PORT')),
    "user": os.getenv('MYSQL_MASTER_USER'),
    "passwd": os.getenv('MYSQL_MASTER_PASS'),
    "db": os.getenv('MYSQL_MASTER_DB')
}

MYSQL_CONFIG_FADE = {
    **MYSQL_CONFIG,
    "db": 'face_recognition'
}

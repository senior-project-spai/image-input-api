# S3
import boto3
from botocore import UNSIGNED
from botocore.client import Config

from app.config import S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET_OBJECT

def upload_fileobj(file, file_name, bucket_name):
    s3_resource = boto3.resource('s3',
                                 endpoint_url=S3_ENDPOINT,
                                 aws_access_key_id=S3_ACCESS_KEY,
                                 aws_secret_access_key=S3_SECRET_KEY,
                                 config=Config(signature_version='s3v4'))
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_fileobj(file, file_name)
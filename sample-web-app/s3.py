import boto3, botocore
from config import *

import passwords

access_key = passwords.access_key
secret_access_key = passwords.secret_access_key

s3 = boto3.client(
   "s3",
   aws_access_key_id=access_key,
   aws_secret_access_key=secret_access_key
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):

    s3.upload_fileobj(
        file,
        bucket_name,
        file.filename,
        ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type
        }
    )




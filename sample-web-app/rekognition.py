import boto3
from config import *

import passwords
access_key = passwords.access_key
secret_access_key = passwords.secret_access_key
s3_region = passwords.s3_region

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region=s3_region):
    rekognition = boto3.client("rekognition", region,
          aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key)
    response = rekognition.detect_labels(
        Image={
          "S3Object": {
            "Bucket": bucket,
            "Name": key,
          }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
      )
    return response['Labels']

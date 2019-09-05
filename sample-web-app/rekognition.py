import boto3
from config import *

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):
    rekognition = boto3.client("rekognition", region,
          aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET)
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

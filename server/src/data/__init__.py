from dataclasses import dataclass
from typing import Protocol

import boto3

S3Key = str

S3Object = str

S3BucketName = str

S3BucketPrefix = str

ContentType = str


class S3ClientWrapper:

    def __init__(self):
        self.__s3_client = boto3.client("s3")

    def put_object(self,
                   bucket: S3BucketName,
                   key: S3Key,
                   body: S3Object,
                   content_type: ContentType) -> None:
        self.__s3_client.put_object(Bucket=bucket,
                                    Key=key,
                                    Body=body,
                                    ContentType=content_type)

    def list_objects_v2(self,
                        bucket: S3BucketName,
                        prefix: S3BucketPrefix) -> list[S3Key]:
        return list(map(lambda x: x['Key'], list(self.__s3_client.list_objects_v2(Bucket=bucket,
                                                                                  Prefix=prefix)['Contents'])))

    def get_object(self,
                   bucket: S3BucketName,
                   key: S3Key) -> S3Object:
        return self.__s3_client.get_object(Bucket=bucket,
                                           Key=key)['Body'].read()

    def delete_object(self,
                      bucket: S3BucketName,
                      key: S3Key) -> None:
        self.__s3_client.delete_object(Bucket=bucket,
                                       Key=key)

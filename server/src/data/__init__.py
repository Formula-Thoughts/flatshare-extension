from dataclasses import dataclass
from typing import Protocol

import boto3


class S3ObjectContent(Protocol):

    def read(self) -> str:
        ...


@dataclass(unsafe_hash=True)
class S3Object(Protocol):
    body: str = None


@dataclass(unsafe_hash=True)
class S3ObjectRef(Protocol):
    key: str = None


@dataclass(unsafe_hash=True)
class S3ObjectRefWrapper(Protocol):
    contents: S3ObjectRef = None


class S3ClientWrapper:

    def __init__(self):
        self.__s3_client = boto3.client("s3")

    def put_object(self,
                   bucket: str,
                   key: str,
                   body: str,
                   content_type: str) -> None:
        self.__s3_client.put_object(Bucket=bucket,
                                    Key=key,
                                    Body=body,
                                    ContentType=content_type)

    def list_objects_v2(self,
                        bucket: str,
                        prefix: str) -> list[S3ObjectRefWrapper]:
        return self.__s3_client.list_objects_v2(Bucket=bucket,
                                                Prefix=prefix)

    def get_object(self,
                   bucket: str,
                   key: str) -> S3Object:
        return self.__s3_client.list_objects_v2(Bucket=bucket,
                                                Key=key)

    def delete_object(self,
                      bucket: str,
                      key: str) -> None:
        self.__s3_client.delete_object(Bucket=bucket,
                                       Key=key)

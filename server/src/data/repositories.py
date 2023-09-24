import os
import typing

from server.src.core import BlobRepo, Serializer, Deserializer
from server.src.data import S3ClientWrapper
from server.src.domain.models import Group

T = typing.TypeVar("T")


class S3BlobRepo(typing.Generic[T]):

    def __init__(self, s3_client_wrapper: S3ClientWrapper,
                 serializer: Serializer,
                 deserializer: Deserializer):
        self.__deserializer = deserializer
        self.__serializer = serializer
        self.__s3_client_wrapper = s3_client_wrapper

    def create(self, data: T, key_gen: typing.Callable[[T], str]) -> None:
        self.__s3_client_wrapper.put_object(bucket=os.environ['S3_BUCKET_NAME'],
                                            key=key_gen(data),
                                            body=self.__serializer.serialize(data.__dict__),
                                            content_type='application/json')


class S3GroupRepo:

    def __init__(self, blob_repo: BlobRepo):
        self.__blob_repo = blob_repo

    def create(self, data: Group) -> None:
        ...
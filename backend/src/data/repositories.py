import os
import typing

from formula_thoughts_web.abstractions import Serializer, Deserializer

from backend.src.core import IBlobRepo, Group
from backend.src.data import S3ClientWrapper

T = typing.TypeVar("T")


class S3BlobRepo(typing.Generic[T]):
    def __init__(
        self,
        s3_client_wrapper: S3ClientWrapper,
        serializer: Serializer,
        deserializer: Deserializer,
    ):
        self.__deserializer = deserializer
        self.__serializer = serializer
        self.__s3_client_wrapper = s3_client_wrapper

    def create(self, data: T, key_gen: typing.Callable[[T], str]) -> None:
        self.__s3_client_wrapper.put_object(
            bucket=os.environ["S3_BUCKET_NAME"],
            key=key_gen(data),
            body=self.__serializer.serialize(data.__dict__),
            content_type="application/json",
        )


class S3GroupRepo:
    def __init__(self, blob_repo: IBlobRepo[Group]):
        self.__blob_repo = blob_repo

    def create(self, group: Group) -> None:
        self.__blob_repo.create(data=group, key_gen=lambda x: f"groups/{x.id}")

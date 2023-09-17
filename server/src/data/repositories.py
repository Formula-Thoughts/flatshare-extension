import json
import os
import typing

from server.src.data import S3ClientWrapper
from server.src.domain.models import Group, Resource

T = typing.TypeVar("T")


class S3BlobRepoBase(typing.Generic[T]):
    __orig_bases__ = None
    __type_name: str

    def __init__(self, s3_client_wrapper):
        self.__s3_client_wrapper: S3ClientWrapper = s3_client_wrapper

    def __init_subclass__(cls) -> None:
        cls.__type_name = typing.get_args(cls.__orig_bases__[0])[0].__name__

    def create(self, data: Resource) -> None:
        self.__s3_client_wrapper.put_object(bucket=os.environ["S3_BUCKET_NAME"],
                                            key=f"{self.__type_name}/{data.id}",
                                            body=json.dumps(data.__dict__, indent=4, sort_keys=True, default=str),
                                            content_type="application/json")

    def get_all(self) -> list[T]:
        ...

    def get_by_id(self, _id: str) -> T:
        ...

    def delete_by_id(self, _id: str) -> None:
        ...


class GroupRepo(S3BlobRepoBase[Group]):
    ...

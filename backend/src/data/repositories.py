import os
import typing

from formula_thoughts_web.abstractions import Serializer, Deserializer
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import IBlobRepo, Group, TData, UserGroups
from src.data import S3ClientWrapper


class S3BlobRepo:
    def __init__(
            self,
            s3_client_wrapper: S3ClientWrapper,
            serializer: Serializer,
            deserializer: Deserializer,
            object_mapper: ObjectMapper
    ):
        self.__object_mapper = object_mapper
        self.__deserializer = deserializer
        self.__serializer = serializer
        self.__s3_client_wrapper = s3_client_wrapper

    def create(self, data: TData, key_gen: typing.Callable[[TData], str]) -> None:
        self.__s3_client_wrapper.put_object(
            bucket=os.environ["S3_BUCKET_NAME"],
            key=key_gen(data),
            body=self.__serializer.serialize(data.__dict__),
            content_type="application/json",
        )

    def get(self, key: str, model_type: typing.Type[TData]) -> TData:
        response = self.__s3_client_wrapper.get_object(bucket=os.environ["S3_BUCKET_NAME"],
                                                       key=key)
        return self.__object_mapper.map_from_dict(_from=self.__deserializer.deserialize(data=response),
                                                  to=model_type)


class S3GroupRepo:
    def __init__(self, blob_repo: IBlobRepo):
        self.__blob_repo = blob_repo

    def create(self, group: Group) -> None:
        self.__blob_repo.create(data=group, key_gen=lambda x: f"groups/{x.id}")

    def get(self, _id: str) -> Group:
        ...


class S3UserGroupsRepo:
    def __init__(self, blob_repo: IBlobRepo):
        self.__blob_repo = blob_repo

    def create(self, user_groups: UserGroups) -> None:
        self.__blob_repo.create(data=user_groups, key_gen=lambda x: f"user_groups/{x.auth_user_id}")

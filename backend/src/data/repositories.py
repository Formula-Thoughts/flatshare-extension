import hashlib
import os
import typing

from apport.user_group import UserGroupID
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
from formula_thoughts_web.abstractions import Serializer, Deserializer
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import IBlobRepo, Group, TData, UserGroups, Property, GroupParticipantName, GroupId, UserId
from src.data import S3ClientWrapper, DynamoDbWrapper, ObjectHasher
from src.exceptions import UserGroupsNotFoundException, GroupNotFoundException


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
            body=self.__serializer.serialize(self.__object_mapper.map_to_dict(_from=data, to=type(data))),
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
        try:
            return self.__blob_repo.get(key=f"groups/{_id}", model_type=Group)
        except ClientError:
            raise GroupNotFoundException()

    def update(self, group: Group) -> None:
        ...

    def add_participant(self, flat: GroupParticipantName) -> None:
        ...


class S3UserGroupsRepo:
    def __init__(self, blob_repo: IBlobRepo):
        self.__blob_repo = blob_repo

    def create(self, user_groups: UserGroups) -> None:
        self.__blob_repo.create(data=user_groups, key_gen=lambda x: f"user_groups/{x.id}")

    def get(self, _id: str) -> UserGroups:
        try:
            return self.__blob_repo.get(key=f"user_groups/{_id}", model_type=UserGroups)
        except ClientError:
            raise UserGroupsNotFoundException()

    def add_group(self, group: GroupId) -> None:
        ...


class DynamoDbUserGroupsRepo:

    def __init__(self, dynamo_wrapper: DynamoDbWrapper,
                 object_mapper: ObjectMapper,
                 object_hasher: ObjectHasher):
        self.__object_hasher = object_hasher
        self.__object_mapper = object_mapper
        self.__dynamo_wrapper = dynamo_wrapper

    def get(self, _id: str) -> UserGroups:
        user_groups = self.__dynamo_wrapper.query(key_condition_expression=
                                                  Key('id').eq(_id) &
                                                  Key('partition_key').eq(f'user_groups:{_id}')
                                              )["Items"][0]
        return self.__object_mapper.map_from_dict(_from=user_groups, to=UserGroups)

    def create(self, user_groups: UserGroups) -> None:
        user_groups.partition_key = self.__partition_key_gen(user_id=user_groups.id)
        user_groups.etag = self.__object_hasher.hash(object=user_groups)
        item = self.__object_mapper.map_to_dict(_from=user_groups, to=UserGroups)
        self.__dynamo_wrapper.put(item=item,
                                  condition_expression=Attr('etag').not_exists())

    def add_group(self, user_id: UserId, etag: str, group: GroupId) -> None:
        self.__dynamo_wrapper.update_item(key={
            "id": user_id,
            "partition_key": f"user_groups:{user_id}"
        },
            update_expression="SET groups = list_append(groups, :i)",
            condition_expression=Attr("etag").eq(etag),
            expression_attribute_values={
                ':i': [group]
            })

    @staticmethod
    def __partition_key_gen(user_id: UserId) -> str:
        return f"user_groups:{user_id}"

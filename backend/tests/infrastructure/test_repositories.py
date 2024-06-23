import os
import uuid
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

import boto3
from autofixture import AutoFixture
from botocore.client import BaseClient
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeDeserializer, ObjectMapper
from moto import mock_aws

from src.core import Group, UserGroups, Property
from src.data import S3ClientWrapper, DynamoDbWrapper, ObjectHasher
from src.data.repositories import S3GroupRepo, S3BlobRepo, S3UserGroupsRepo, DynamoDbUserGroupsRepo, DynamoDbGroupRepo, \
    DynamoDbPropertyRepo
from src.exceptions import GroupNotFoundException, UserGroupsNotFoundException

BUCKET = "test-bucket"


class S3TestCase(TestCase):

    def _set_up_bucket(self):
        self.__s3 = boto3.client('s3')
        self.__s3_client_wrapper = S3ClientWrapper(client=self.__s3)
        self._blob_repo = S3BlobRepo(s3_client_wrapper=self.__s3_client_wrapper,
                                     serializer=JsonSnakeToCamelSerializer(),
                                     deserializer=JsonCamelToSnakeDeserializer(),
                                     object_mapper=ObjectMapper())
        self.__s3.create_bucket(Bucket=BUCKET,
                                CreateBucketConfiguration={
                                    'LocationConstraint': 'eu-west-2',
                                })


class DynamoDbTestCase(TestCase):

    def _set_up_table(self):
        table_name = 'flatini-test'
        self.__dynamo = boto3.resource('dynamodb')
        self._dynamo_client_wrapper = DynamoDbWrapper(dynamo_client=self.__dynamo, tablename=table_name)
        self.__dynamo.create_table(TableName=table_name,
                                   KeySchema=[
                                       {
                                           'AttributeName': 'partition_key',
                                           'KeyType': 'HASH',
                                       },
                                       {
                                           'AttributeName': 'id',
                                           'KeyType': 'RANGE',
                                       }
                                   ],
                                   AttributeDefinitions=[
                                       {
                                           'AttributeName': 'partition_key',
                                           'AttributeType': 'S'
                                       },
                                       {
                                           'AttributeName': 'id',
                                           'AttributeType': 'S'
                                       }
                                   ],
                                   BillingMode='PAY_PER_REQUEST')


class TestS3GroupRepo(S3TestCase):

    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_by_id(self):
        # arrange
        self._set_up_bucket()
        sut = S3GroupRepo(blob_repo=self._blob_repo)
        stored_group = AutoFixture().create(dto=Group)
        sut.create(group=stored_group)

        # act
        fetched_group = sut.get(_id=stored_group.id)

        # assert
        self.assertEqual(fetched_group, stored_group)

    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_by_id_when_not_found(self):
        # arrange
        self._set_up_bucket()
        sut = S3GroupRepo(blob_repo=self._blob_repo)

        # act/assert
        with self.assertRaises(expected_exception=GroupNotFoundException):
            sut.get(_id=str(uuid.uuid4()))


class TestS3UserGroupsRepo(S3TestCase):

    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_by_auth_id(self):
        # arrange
        self._set_up_bucket()
        sut = S3UserGroupsRepo(blob_repo=self._blob_repo)
        stored_user_groups = AutoFixture().create(dto=UserGroups)
        sut.create(user_groups=stored_user_groups)

        # act
        fetched_user_groups = sut.get(_id=stored_user_groups.id)

        # assert
        self.assertEqual(fetched_user_groups, stored_user_groups)

    @mock_aws
    @patch.dict(os.environ, {
        "S3_BUCKET_NAME": BUCKET,
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_by_auth_id_when_not_found(self):
        # arrange
        self._set_up_bucket()
        sut = S3UserGroupsRepo(blob_repo=self._blob_repo)

        # act/assert
        with self.assertRaises(expected_exception=UserGroupsNotFoundException):
            sut.get(_id=str(uuid.uuid4()))


class TestGroupRepo(DynamoDbTestCase):

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_retrieves_user_group(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher: ObjectHasher = Mock()
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        hash = "test hash"
        object_hasher.hash = MagicMock(return_value=hash)
        user_groups = AutoFixture().create(dto=UserGroups)
        sut.create(user_groups=user_groups)

        # act
        received_user_groups = sut.get(_id=user_groups.id)
        user_groups.etag = hash
        user_groups.partition_key = f"user_groups:{user_groups.id}"

        # assert
        with self.subTest(msg="assert correct user groups document was received"):
            self.assertEqual(received_user_groups, user_groups)

        # assert
        with self.subTest(msg="assert hasher was called once"):
            object_hasher.hash.assert_called_once()

        # assert
        with self.subTest(msg="assert hasher was called with correct args"):
            object_hasher.hash.assert_called_with(object=user_groups)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_group_adds_group_to_user_groups(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher: ObjectHasher = Mock()
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        user_groups = AutoFixture().create(dto=UserGroups)
        object_hasher.hash = MagicMock(return_value="hash")
        sut.create(user_groups=user_groups)
        group_to_add = str(uuid.uuid4())

        # act
        sut.add_group(group=group_to_add, user_groups=user_groups)
        received_user_groups = sut.get(_id=user_groups.id)

        # assert
        with self.subTest(msg="assert document was updated"):
            self.assertEqual(received_user_groups.groups, [*user_groups.groups, group_to_add])

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_properties(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher: ObjectHasher = Mock()
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        prop_repo = DynamoDbPropertyRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                   object_mapper=object_mapper,
                                   object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        props: list[Property] = AutoFixture().create_many(dto=Property, ammount=3)
        hash_value = "hash"
        object_hasher.hash = MagicMock(return_value=hash_value)
        sut.create(group=group)
        for prop in props:
            prop_repo.create(group_id=group.id, property=prop)

        # act
        group_properties = sut.get(_id=group.id)

        group.etag = hash_value
        group.partition_key = f"group:{group.id}"
        group
        for prop in props:
            prop.etag = hash_value
            prop.partition_key = f"group:{group.id}:flat"

        # assert
        with self.subTest(msg="assert group properties were received"):
            self.assertEqual(group_properties.groups, [*user_groups.groups, group_to_add])

import os
import uuid
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

import boto3
from autofixture import AutoFixture
from botocore.client import BaseClient
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, JsonCamelToSnakeDeserializer, ObjectMapper
from moto import mock_aws

from src.core import Group, UserGroups, Property, GroupProperties
from src.data import S3ClientWrapper, DynamoDbWrapper, ObjectHasher
from src.data.repositories import S3GroupRepo, S3BlobRepo, S3UserGroupsRepo, DynamoDbUserGroupsRepo, DynamoDbGroupRepo, \
    DynamoDbPropertyRepo
from src.exceptions import GroupNotFoundException, UserGroupsNotFoundException, ConflictException, \
    GroupAlreadyExistsException, UserGroupAlreadyExistsException

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


class TestUserGroupRepo(DynamoDbTestCase):

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_retrieves_user_group(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        user_groups = AutoFixture().create(dto=UserGroups)
        user_groups.etag = None
        sut.create(user_groups=user_groups)

        # act
        received_user_groups = sut.get(_id=user_groups.id)
        user_groups.etag = None
        user_groups.etag = object_hasher.hash(user_groups)

        # assert
        with self.subTest(msg="assert correct user groups document was received"):
            self.assertEqual(received_user_groups, user_groups)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_create_user_groups_should_throw_when_already_exists(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        user_groups = AutoFixture().create(dto=UserGroups)
        sut.create(user_groups=user_groups)

        # act
        sut_call = lambda: sut.create(user_groups=user_groups)

        # assert
        with self.subTest(msg="assert user group already exists error is thrown"):
            with self.assertRaises(expected_exception=UserGroupAlreadyExistsException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_user_groups_throw_when_not_found(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)

        # act
        sut_call = lambda: sut.get(_id=str(uuid.uuid4()))

        # assert
        with self.subTest(msg="assert user groups not found error is thrown"):
            with self.assertRaises(expected_exception=UserGroupsNotFoundException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_group_adds_group_to_user_groups(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        user_groups = AutoFixture().create(dto=UserGroups)
        sut.create(user_groups=user_groups)
        group_to_add = str(uuid.uuid4())

        # act
        sut.add_group(group=group_to_add, user_groups=user_groups)
        received_user_groups = sut.get(_id=user_groups.id)

        # assert
        with self.subTest(msg="assert document was updated"):
            self.assertEqual(received_user_groups.groups, user_groups.groups)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_group_adds_group_to_user_groups_when_precondition_check_fails(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        user_groups = AutoFixture().create(dto=UserGroups)
        sut.create(user_groups=user_groups)
        group_to_add = str(uuid.uuid4())

        # act
        sut.add_group(group=str(uuid.uuid4()), user_groups=user_groups)
        sut_call = lambda: sut.add_group(group=group_to_add, user_groups=user_groups)

        # assert
        with self.subTest(msg="assert conflict exception is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_group_adds_group_to_user_groups_when_not_found(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                     object_mapper=object_mapper,
                                     object_hasher=object_hasher)
        user_groups = AutoFixture().create(dto=UserGroups)

        # act
        sut_call = lambda: sut.add_group(group=str(uuid.uuid4()), user_groups=user_groups)

        # assert
        with self.subTest(msg="assert conflict exception is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()


class TestGroupRepo(DynamoDbTestCase):

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_properties(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        prop_repo = DynamoDbPropertyRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                         object_mapper=object_mapper,
                                         object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        group.etag = None
        group.partition_key = None
        group_id = group.id
        props: list[Property] = AutoFixture().create_many(dto=Property, ammount=3)
        sut.create(group=group)
        group.etag = None
        group.id = f"group:{group_id}"
        group_hash = object_hasher.hash(group)
        for prop in props:
            prop_repo.create(group_id=group_id, property=prop)

        # act
        group_properties = sut.get(_id=group_id)

        expected_group_properties = GroupProperties(etag=group_hash,
                                                    partition_key=f"group:{group_id}",
                                                    id=group_id,
                                                    participants=group.participants,
                                                    price_limit=group.price_limit,
                                                    locations=group.locations,
                                                    properties=props)
        expected_group_properties.properties.sort(key=lambda x: x.id)
        group_properties.properties.sort(key=lambda x: x.id)

        # assert
        with self.subTest(msg="assert expected group properties were received"):
            self.assertEqual(group_properties, expected_group_properties)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_create_group_where_group_already_exists(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        sut.create(group=group)

        # act
        sutcall = lambda: sut.create(group=group)

        with self.subTest(msg="assert group already exists"):
            with self.assertRaises(expected_exception=GroupAlreadyExistsException):
                sutcall()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_properties_when_no_properties(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        group.etag = None
        group_id = group.id
        sut.create(group=group)
        group.etag = None
        group.id = f"group:{group_id}"
        group_hash = object_hasher.hash(group)

        # act
        group_properties = sut.get(_id=group_id)

        expected_group_properties = GroupProperties(etag=group_hash,
                                                    partition_key=f"group:{group_id}",
                                                    id=group_id,
                                                    participants=group.participants,
                                                    price_limit=group.price_limit,
                                                    locations=group.locations,
                                                    properties=[])

        # assert
        with self.subTest(msg="assert expected group properties were received"):
            self.assertEqual(group_properties, expected_group_properties)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_get_group_properties_should_throw_when_not_found(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)

        # act
        sut_call = lambda: sut.get(_id=str(uuid.uuid4()))

        # assert
        with self.subTest(msg="assert group was not found"):
            with self.assertRaises(expected_exception=GroupNotFoundException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_update_group(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        group_id = group.id
        sut.create(group=group)
        prev_etag = group.etag
        new_price = Decimal('123.2')
        new_locations = ["DT1", "Dorchester"]
        group.price_limit = new_price
        group.locations = new_locations
        sut.update(group=group)
        group.etag = prev_etag
        group.id = f"group:{group_id}"
        group_hash = object_hasher.hash(group)

        # act
        group_properties = sut.get(_id=group_id)

        expected_group_properties = GroupProperties(etag=group_hash,
                                                    partition_key=f"group:{group_id}",
                                                    id=group_id,
                                                    participants=group.participants,
                                                    price_limit=new_price,
                                                    locations=new_locations,
                                                    properties=[])

        # assert
        with self.subTest(msg="assert expected groups were received"):
            self.assertEqual(group_properties, expected_group_properties)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_update_group_when_not_found(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        sut.update(group=group)

        # act
        sut_call = lambda: sut.get(_id=group.id)

        # assert
        with self.subTest(msg="assert conflict is thrown"):
            with self.assertRaises(ConflictException):
                sut_call()

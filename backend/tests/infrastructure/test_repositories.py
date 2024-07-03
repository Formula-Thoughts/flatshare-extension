import os
import uuid
from copy import copy
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

import boto3
from autofixture import AutoFixture
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, ObjectMapper
from moto import mock_aws

from src.core import Group, UserGroups, Property, GroupProperties
from src.data import DynamoDbWrapper, ObjectHasher
from src.data.repositories import DynamoDbUserGroupsRepo, DynamoDbGroupRepo, \
    DynamoDbPropertyRepo, DynamoDbRedFlagRepo
from src.exceptions import GroupNotFoundException, UserGroupsNotFoundException, ConflictException, \
    GroupAlreadyExistsException, UserGroupAlreadyExistsException, PropertyNotFoundException


class DynamoDbTestCase(TestCase):

    def _set_up_table(self):
        table_name = 'flatini-test'
        self.__dynamo = boto3.resource('dynamodb', region_name="eu-west-2")
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

        # act
        sut_call = lambda: sut.update(group=group)

        # assert
        with self.subTest(msg="assert conflict is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_update_group_when_conflict(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        sut.create(group=group)
        prev_etag = group.etag
        group.price_limit = Decimal("123.4")
        sut.update(group=group)

        # act
        group.etag = prev_etag
        group.price_limit = Decimal("123.5")
        sut_call = lambda: sut.update(group=group)

        # assert
        with self.subTest(msg="assert conflict is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_participant(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        prev_participants = copy(group.participants)
        group_id = group.id
        sut.create(group=group)
        participant_to_add = "Bob Marley"
        sut.add_participant(participant=participant_to_add, group=group)
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
        with self.subTest(msg="assert expected groups were received"):
            self.assertEqual(group_properties, expected_group_properties)

        # assert
        with self.subTest(msg="assert participant was added"):
            self.assertEqual([*prev_participants, participant_to_add], group.participants)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_participant_when_not_found(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        participant_to_add = "Bob Marley"

        # act
        sut_call = lambda: sut.add_participant(participant=participant_to_add, group=group)

        # assert
        with self.subTest(msg="assert conflict error is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_add_participant_when_conflict(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                object_mapper=object_mapper,
                                object_hasher=object_hasher)
        group = AutoFixture().create(dto=Group)
        sut.create(group=group)
        sut.add_participant(participant="Aidan Gannon", group=group)

        # act
        sut_call = lambda: sut.add_participant(participant="Dom Farr", group=group)

        # assert
        with self.subTest(msg="assert conflict is raised"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()


class TestPropertyRepo(DynamoDbTestCase):

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_delete_property(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbPropertyRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                   object_mapper=object_mapper,
                                   object_hasher=object_hasher)
        property = AutoFixture().create(dto=Property)
        group_id = str(uuid.uuid4())
        sut.create(group_id=group_id, property=property)

        # act
        sut.delete(group_id=group_id, property_id=property.id)

        items = self._dynamo_client_wrapper.query(
            key_condition_expression="partition_key = :partition_key and id = :id",
            expression_attribute_values={
                ":id": f"property:{property.id}",
                ":partition_key": f"group:{group_id}"
            })["Items"]

        # assert
        with self.subTest(msg="assert property is not found"):
            self.assertEqual(len(items), 0)

    @mock_aws
    @patch.dict(os.environ, {
        "AWS_ACCESS_KEY_ID": "test",
        "AWS_SECRET_ACCESS_KEY": "test"
    }, clear=True)
    def test_delete_property_when_not_found(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbPropertyRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                   object_mapper=object_mapper,
                                   object_hasher=object_hasher)

        # act
        sut_call = lambda: sut.delete(group_id=str(uuid.uuid4()), property_id=str(uuid.uuid4()))

        # assert
        with self.subTest(msg="assert property is not found"):
            with self.assertRaises(expected_exception=PropertyNotFoundException):
                sut_call()


class TestRedFlagsRepo(DynamoDbTestCase):

    def test_create(self):
        # arrange
        self._set_up_table()
        object_mapper = ObjectMapper()
        object_hasher = ObjectHasher(object_mapper=object_mapper, serializer=JsonSnakeToCamelSerializer())
        sut = DynamoDbRedFlagRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                  object_mapper=object_mapper,
                                  object_hasher=object_hasher)

        # act


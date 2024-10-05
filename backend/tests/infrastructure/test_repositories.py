import os
import uuid
from copy import copy, deepcopy
from decimal import Decimal
from unittest.mock import patch

from autofixture import AutoFixture
from formula_thoughts_web.crosscutting import JsonSnakeToCamelSerializer, ObjectMapper
from moto import mock_aws

from src.core import Group, UserGroups, Property, GroupProperties, RedFlag
from src.infra import ObjectHasher
from src.infra.repositories import DynamoDbUserGroupsRepo, DynamoDbGroupRepo, \
    DynamoDbPropertyRepo, DynamoDbRedFlagRepo
from src.exceptions import GroupNotFoundException, UserGroupsNotFoundException, ConflictException, \
    GroupAlreadyExistsException, UserGroupAlreadyExistsException, PropertyNotFoundException, \
    RedFlagAlreadyExistsException, RedFlagNotFoundException
from tests.infrastructure import DynamoDbTestCase


@mock_aws
class TestUserGroupRepo(DynamoDbTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__sut = DynamoDbUserGroupsRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                            object_mapper=self._object_mapper,
                                            object_hasher=self._object_hasher)

    def test_get_user_groups_retrieves_user_group(self):
        # arrange
        user_groups = AutoFixture().create(dto=UserGroups)
        user_groups.etag = None
        self.__sut.create(user_groups=user_groups)

        # act
        received_user_groups = self.__sut.get(_id=user_groups.id)
        user_groups.etag = None
        user_groups.etag = self._object_hasher.hash(user_groups)

        # assert
        with self.subTest(msg="assert correct user groups document was received"):
            self.assertEqual(received_user_groups, user_groups)

    def test_create_user_groups_should_throw_when_already_exists(self):
        # arrange
        user_groups = AutoFixture().create(dto=UserGroups)
        self.__sut.create(user_groups=user_groups)

        # act
        sut_call = lambda: self.__sut.create(user_groups=user_groups)

        # assert
        with self.subTest(msg="assert user group already exists error is thrown"):
            with self.assertRaises(expected_exception=UserGroupAlreadyExistsException):
                sut_call()

    def test_get_user_groups_throw_when_not_found(self):
        # act
        sut_call = lambda: self.__sut.get(_id=str(uuid.uuid4()))

        # assert
        with self.subTest(msg="assert user groups not found error is thrown"):
            with self.assertRaises(expected_exception=UserGroupsNotFoundException):
                sut_call()

    def test_add_group_adds_group_to_user_groups(self):
        # arrange
        user_groups = AutoFixture().create(dto=UserGroups)
        self.__sut.create(user_groups=user_groups)
        group_to_add = str(uuid.uuid4())

        # act
        self.__sut.add_group(group=group_to_add, user_groups=user_groups)
        received_user_groups = self.__sut.get(_id=user_groups.id)

        # assert
        with self.subTest(msg="assert document was updated"):
            self.assertEqual(received_user_groups.groups, user_groups.groups)

    def test_add_group_adds_group_to_user_groups_when_precondition_check_fails(self):
        # arrange
        user_groups = AutoFixture().create(dto=UserGroups)
        self.__sut.create(user_groups=user_groups)
        old_etag = user_groups.etag
        group_to_add = str(uuid.uuid4())

        # act
        self.__sut.add_group(group=str(uuid.uuid4()), user_groups=user_groups)
        user_groups.etag = old_etag
        sut_call = lambda: self.__sut.add_group(group=group_to_add, user_groups=user_groups)

        # assert
        with self.subTest(msg="assert conflict exception is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    def test_add_group_adds_group_to_user_groups_when_not_found(self):
        # arrange
        user_groups = AutoFixture().create(dto=UserGroups)

        # act
        sut_call = lambda: self.__sut.add_group(group=str(uuid.uuid4()), user_groups=user_groups)

        # assert
        with self.subTest(msg="assert conflict exception is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()


@mock_aws
class TestGroupRepo(DynamoDbTestCase):

    def setUp(self):
        super().setUp()
        self.__sut = DynamoDbGroupRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                       object_mapper=self._object_mapper,
                                       object_hasher=self._object_hasher)
        self.__prop_repo = DynamoDbPropertyRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                                object_mapper=self._object_mapper,
                                                object_hasher=self._object_hasher)

    def test_get_group_properties(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        group.etag = None
        group.partition_key = None
        group_id = group.id
        props: list[Property] = AutoFixture().create_many(dto=Property, ammount=3)
        self.__sut.create(group=group)
        group.etag = None
        group.id = f"group:{group_id}"
        group_hash = self._object_hasher.hash(group)
        for prop in props:
            self.__prop_repo.create(group_id=group_id, property=prop)

        # act
        group_properties = self.__sut.get(_id=group_id)

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

    def test_create_group_where_group_already_exists(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        self.__sut.create(group=group)

        # act
        sutcall = lambda: self.__sut.create(group=group)

        with self.subTest(msg="assert group already exists"):
            with self.assertRaises(expected_exception=GroupAlreadyExistsException):
                sutcall()

    def test_get_group_properties_when_no_properties(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        group.etag = None
        group_id = group.id
        self.__sut.create(group=group)
        group.etag = None
        group.id = f"group:{group_id}"
        group_hash = self._object_hasher.hash(group)

        # act
        group_properties = self.__sut.get(_id=group_id)

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

    def test_get_group_properties_should_throw_when_not_found(self):
        # act
        sut_call = lambda: self.__sut.get(_id=str(uuid.uuid4()))

        # assert
        with self.subTest(msg="assert group was not found"):
            with self.assertRaises(expected_exception=GroupNotFoundException):
                sut_call()

    def test_update_group(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        group_id = group.id
        self.__sut.create(group=group)
        prev_etag = group.etag
        new_price = Decimal('123.2')
        new_locations = ["DT1", "Dorchester"]
        group.price_limit = new_price
        group.locations = new_locations
        self.__sut.update(group=group)
        group.etag = prev_etag
        group.id = f"group:{group_id}"
        group_hash = self._object_hasher.hash(group)

        # act
        group_properties = self.__sut.get(_id=group_id)

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

    def test_update_group_when_not_found(self):
        # arrange
        group = AutoFixture().create(dto=Group)

        # act
        sut_call = lambda: self.__sut.update(group=group)

        # assert
        with self.subTest(msg="assert conflict is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    def test_update_group_when_conflict(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        self.__sut.create(group=group)
        prev_etag = group.etag
        group.price_limit = Decimal("123.4")
        self.__sut.update(group=group)

        # act
        group.etag = prev_etag
        group.price_limit = Decimal("123.5")
        sut_call = lambda: self.__sut.update(group=group)

        # assert
        with self.subTest(msg="assert conflict is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    def test_add_participant(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        prev_participants = copy(group.participants)
        group_id = group.id
        self.__sut.create(group=group)
        participant_to_add = "Bob Marley"
        self.__sut.add_participant(participant=participant_to_add, group=group)

        # act
        group_properties = self.__sut.get(_id=group_id)

        expected_group_properties = GroupProperties(etag=group.etag,
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

    def test_add_participant_when_not_found(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        participant_to_add = "Bob Marley"

        # act
        sut_call = lambda: self.__sut.add_participant(participant=participant_to_add, group=group)

        # assert
        with self.subTest(msg="assert conflict error is thrown"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    def test_add_participant_when_conflict(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        self.__sut.create(group=group)
        old_etag = group.etag
        self.__sut.add_participant(participant="Aidan Gannon", group=group)
        group.etag = old_etag

        # act
        sut_call = lambda: self.__sut.add_participant(participant="Dom Farr", group=group)

        # assert
        with self.subTest(msg="assert conflict is raised"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()


@mock_aws
class TestPropertyRepo(DynamoDbTestCase):

    def setUp(self):
        super().setUp()
        self.__sut = DynamoDbPropertyRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                          object_mapper=self._object_mapper,
                                          object_hasher=self._object_hasher)

    def test_delete_property(self):
        # arrange
        property = AutoFixture().create(dto=Property)
        group_id = str(uuid.uuid4())
        self.__sut.create(group_id=group_id, property=property)

        # act
        self.__sut.delete(group_id=group_id, property_id=property.id)

        items = self._dynamo_client_wrapper.query(
            key_condition_expression="partition_key = :partition_key and id = :id",
            expression_attribute_values={
                ":id": f"property:{property.id}",
                ":partition_key": f"group:{group_id}"
            })["Items"]

        # assert
        with self.subTest(msg="assert property is not found"):
            self.assertEqual(len(items), 0)

    def test_delete_property_when_not_found(self):
        # act
        sut_call = lambda: self.__sut.delete(group_id=str(uuid.uuid4()), property_id=str(uuid.uuid4()))

        # assert
        with self.subTest(msg="assert property is not found"):
            with self.assertRaises(expected_exception=PropertyNotFoundException):
                sut_call()


@mock_aws
class TestRedFlagsRepo(DynamoDbTestCase):

    def setUp(self):
        super().setUp()
        self.__sut = DynamoDbRedFlagRepo(dynamo_wrapper=self._dynamo_client_wrapper,
                                         object_mapper=self._object_mapper,
                                         object_hasher=self._object_hasher)

    def test_create(self):
        # arrange
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__sut.create(red_flag=red_flag)

        # act
        red_flags = self.__sut.get_by_url(property_url=red_flag.property_url)

        # assert
        with self.subTest(msg="assert 1 red flag is received"):
            self.assertEqual(len(red_flags), 1)

        # assert
        with self.subTest(msg="assert correct red flag is received"):
            self.assertEqual(red_flags[0], red_flag)

    def test_create_when_already_exists(self):
        # arrange
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__sut.create(red_flag=red_flag)

        # act
        sut_call = lambda: self.__sut.create(red_flag=red_flag)

        # assert
        with self.subTest(msg="assert red flag already exists error is thrown"):
            with self.assertRaises(expected_exception=RedFlagAlreadyExistsException):
                sut_call()

    def test_get_when_none_exist(self):
        # act
        red_flags = self.__sut.get_by_url(property_url="fsda")

        # assert
        with self.subTest(msg="assert red flags are empty"):
            self.assertEqual(len(red_flags), 0)

    def test_get_by_id(self):
        # arrange
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__sut.create(red_flag=red_flag)

        # act
        returned_red_flag = self.__sut.get(property_url=red_flag.property_url, _id=red_flag.id)

        # assert
        with self.subTest(msg="assert red flag is returned"):
            self.assertEqual(returned_red_flag, red_flag)

    def test_get_by_id_when_not_found(self):
        # act
        sut_call = lambda: self.__sut.get(property_url="blah", _id="testid")

        # assert
        with self.subTest(msg="assert red flag not found is raised"):
            with self.assertRaises(expected_exception=RedFlagNotFoundException):
                sut_call()

    def test_add_voter(self):
        # arrange
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__sut.create(red_flag)
        expected_red_flag = deepcopy(red_flag)
        user = "1234"
        expected_red_flag.votes.append(user)
        self.__sut.add_voter(user, red_flag)
        expected_red_flag.etag = red_flag.etag

        # act
        returned_red_flag = self.__sut.get(red_flag.property_url, red_flag.id)

        # assert
        with self.subTest(msg="returned red flag equals expected"):
            self.assertEqual(expected_red_flag, returned_red_flag)

        # assert
        with self.subTest(msg="propagated object equals expected"):
            self.assertEqual(expected_red_flag, red_flag)

    def test_add_voter_when_conflict(self):
        # arrange
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__sut.create(red_flag)
        old_etag = red_flag.etag
        user = "1234"
        self.__sut.add_voter(user, red_flag)

        # act
        red_flag.etag = old_etag
        sut_call = lambda: self.__sut.add_voter(user, red_flag)

        # assert
        with self.subTest(msg="conflict error is raised"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

    def test_remove_voter(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        red_flag.votes.append(user)
        self.__sut.create(red_flag)
        expected_red_flag = deepcopy(red_flag)
        expected_red_flag.votes.remove(user)
        self.__sut.remove_voter(user, red_flag)
        expected_red_flag.etag = red_flag.etag

        # act
        returned_red_flag = self.__sut.get(red_flag.property_url, red_flag.id)

        # assert
        with self.subTest(msg="returned red flag equals expected"):
            self.assertEqual(expected_red_flag, returned_red_flag)

        # assert
        with self.subTest(msg="propagated object equals expected"):
            self.assertEqual(expected_red_flag, red_flag)

    def test_remove_voter_when_conflict(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        red_flag.votes.append(user)
        red_flag.votes.append(user)
        self.__sut.create(red_flag)
        old_etag = red_flag.etag
        self.__sut.remove_voter(user, red_flag)

        # act
        red_flag.etag = old_etag
        sut_call = lambda: self.__sut.remove_voter(user, red_flag)

        # assert
        with self.subTest(msg="conflict error is raised"):
            with self.assertRaises(expected_exception=ConflictException):
                sut_call()

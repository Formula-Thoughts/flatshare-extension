import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call
from uuid import UUID

from autofixture import AutoFixture
from callee import Any, Captor
from ddt import ddt, data
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper
from formula_thoughts_web.events import SQSEventPublisher, EVENT

from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, \
    CreateGroupAsyncCommand, UpsertGroupBackgroundCommand, UpsertUserGroupsBackgroundCommand, \
    CreateUserGroupsAsyncCommand, FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand
from src.domain.errors import invalid_price_error, UserGroupsNotFoundError
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse
from src.exceptions import UserGroupsNotFoundException

UUID_EXAMPLE = "723f9ec2-fec1-4616-9cf2-576ee632822d"


class TestSetGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetGroupRequestCommand(object_mapper=ObjectMapper())

    def test_run(self):
        # arrange
        location = "UK"
        price_limit = 14.2
        context = ApplicationContext(variables={},
                                     body={"price_limit": price_limit, "location": location})

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="group request is set"):
            create_group_request = context.get_var("UPSERT_GROUP_REQUEST", UpsertGroupRequest)
            self.assertEqual(create_group_request.location, location)
            self.assertEqual(create_group_request.price_limit, price_limit)


@ddt
class TestValidateGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateGroupCommand()

    def test_run_with_valid_data(self):
        # arrange
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=14.4, location="UK")
        })

        # act
        self.__sut.run(context)

        # assert
        self.assertEqual(context.error_capsules, [])

    @data([0], [-14])
    def test_run_with_invalid_data(self, price):
        # arrange
        [price_limit] = price
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=price_limit, location="UK")
        })

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="assert 1 error capsule is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="asser price error capsule is added"):
            self.assertEqual(context.error_capsules[0], invalid_price_error)


class TestSaveGroupAsyncOverSQSCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = CreateGroupAsyncCommand(sqs_event_publisher=self.__sqs_event_publisher)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    def test_run_should_publish_to_sqs(self, _) -> None:
        # arrange
        group_request = AutoFixture().create(dto=UpsertGroupRequest)
        auth_user_id = "12345"
        expected_group = Group(id=UUID_EXAMPLE,
                               price_limit=group_request.price_limit,
                               location=group_request.location,
                               flats=[],
                               participants=[auth_user_id])
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: group_request
        },
            auth_user_id=auth_user_id)
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert sqs message is sent once"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="assert sqs message is sent with correct params"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=UUID_EXAMPLE,
                                                                           payload=Group(
                                                                               id=UUID_EXAMPLE,
                                                                               price_limit=group_request.price_limit,
                                                                               location=group_request.location,
                                                                               flats=[],
                                                                               participants=[auth_user_id]
                                                                           ))

        # assert
        with self.subTest(msg="assert response is set to group"):
            self.assertEqual(CreatedGroupResponse(group=expected_group), context.response)

        # assert
        with self.subTest(msg="assert group id is saved as context var"):
            self.assertEqual(context.get_var("GROUP_ID", str), UUID_EXAMPLE)


class TestSaveUserGroupsAsyncOverSQSCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = CreateUserGroupsAsyncCommand(sqs_event_publisher=self.__sqs_event_publisher)

    def test_run_should_publish_to_sqs(self) -> None:
        # arrange
        group_id = str(uuid.uuid4())
        auth_user_id = "12345"
        expected_user_group = UserGroups(auth_user_id=auth_user_id,
                                         groups=[group_id])
        context = ApplicationContext(variables={GROUP_ID: group_id}, auth_user_id=auth_user_id)
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert sqs message is sent once"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="assert sqs message is sent with correct params"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=auth_user_id,
                                                                           payload=expected_user_group)


class TestUpsertGroupBackgroundCommand(TestCase):

    def setUp(self):
        self.__group_repo: IGroupRepo = Mock()
        self.__sut = UpsertGroupBackgroundCommand(group_repo=self.__group_repo)

    def test_run_should_upsert_group(self):
        # arrange
        self.__group_repo.create = MagicMock()
        event = AutoFixture().create(dto=Group)
        context = ApplicationContext(variables={EVENT: event})

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert group is stored once"):
            self.__group_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="assert group is stored with valid params"):
            self.__group_repo.create.assert_called_with(group=event)


class TestUpsertUserGroupsBackgroundCommand(TestCase):

    def setUp(self):
        self.__user_groups_repo: IUserGroupsRepo = Mock()
        self.__sut = UpsertUserGroupsBackgroundCommand(user_groups_repo=self.__user_groups_repo)

    def test_run_should_upsert_group(self):
        # arrange
        self.__user_groups_repo.create = MagicMock()
        event = AutoFixture().create(dto=UserGroups)
        context = ApplicationContext(variables={EVENT: event})

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert group is stored once"):
            self.__user_groups_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="assert group is stored with valid params"):
            self.__user_groups_repo.create.assert_called_with(user_groups=event)


class TestFetchUserGroupsCommand(TestCase):

    def setUp(self):
        self.__group_repo: IGroupRepo = Mock()
        self.__user_groups_repo: IUserGroupsRepo = Mock()
        self.__sut = FetchUserGroupsCommand(group_repo=self.__group_repo, user_group_repo=self.__user_groups_repo)

    def test_run_should_fetch_groups_for_auth_user(self):
        # arrange
        auth_user_id = "12345"
        context = ApplicationContext(auth_user_id=auth_user_id, variables={})
        user_groups = AutoFixture().create(dto=UserGroups)
        user_groups.groups = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
        groups = AutoFixture().create_many(dto=Group, ammount=3)
        self.__user_groups_repo.get = MagicMock(return_value=user_groups)
        self.__group_repo.get = MagicMock(side_effect=groups)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest("assert response is set to groups"):
            self.assertEqual(context.response, ListUserGroupsResponse(groups=groups))

        # assert
        with self.subTest("assert groups is set as context var"):
            self.assertEqual(context.get_var("USER_GROUPS", list[Group]), groups)

        # assert
        with self.subTest("assert user groups repo is called once"):
            self.__user_groups_repo.get.assert_called_once()

        # assert
        with self.subTest("assert user groups repo is called with auth user id"):
            self.__user_groups_repo.get.assert_called_with(_id=auth_user_id)

        # assert
        with self.subTest("assert group repo is called 3 times for each group"):
            self.__group_repo.get.assert_has_calls([
                call(_id=user_groups.groups[0]),
                call(_id=user_groups.groups[1]),
                call(_id=user_groups.groups[2])
            ])

    def test_run_should_error_when_user_groups_cannot_be_found(self):
        # arrange
        auth_user_id = "12345"
        context = ApplicationContext(auth_user_id=auth_user_id, variables={})
        self.__user_groups_repo.get = MagicMock(side_effect=UserGroupsNotFoundException())
        self.__group_repo.get = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest("assert error is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest("assert error is user group not found"):
            self.assertEqual(type(context.error_capsules[0]), UserGroupsNotFoundError)

        # assert
        with self.subTest("assert user groups repo is never called"):
            self.__group_repo.get.assert_not_called()


class TestValidateIfUserBelongsToAtLeastOneGroupCommand(TestCase):

    def setUp(self):
        self.__user_groups_repo: IUserGroupsRepo = Mock()
        self.__sut = ValidateIfUserBelongsToAtLeastOneGroupCommand(user_groups_repo=self.__user_groups_repo)

    def test_run_when_user_has_at_least_one_group(self):
        # arrange
        auth_user_id = "1235"
        context = ApplicationContext(auth_user_id=auth_user_id)
        user_groups = AutoFixture().create(dto=UserGroups)
        self.__user_groups_repo.get = MagicMock(return_value=user_groups)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest("repo is called once"):
            self.__user_groups_repo.get.assert_called_once()

        # assert
        with self.subTest("repo is called with args"):
            self.__user_groups_repo.get.assert_called_with(_id=auth_user_id)

        # assert
        with self.subTest("user groups is set as context var"):
            self.assertEqual(context.get_var("USER_GROUPS", UserGroups), user_groups)

        # assert
        with self.subTest("validation result is set as context var"):
            self.assertEqual(context.get_var("USER_BELONGS_TO_AT_LEAST_ONE_GROUP", bool), True)

    def test_run_when_user_has_no_groups(self):
        # arrange
        auth_user_id = "1235"
        context = ApplicationContext(auth_user_id=auth_user_id)
        user_groups = AutoFixture().create(dto=UserGroups)
        self.__user_groups_repo.get = MagicMock(return_value=user_groups)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest("repo is called once"):
            self.__user_groups_repo.get.assert_called_once()

        # assert
        with self.subTest("repo is called with args"):
            self.__user_groups_repo.get.assert_called_with(_id=auth_user_id)

        # assert
        with self.subTest("user groups is set as context var"):
            self.assertEqual(context.get_var("USER_GROUPS", UserGroups), user_groups)

        # assert
        with self.subTest("validation result is set as context var"):
            self.assertEqual(context.get_var("USER_BELONGS_TO_AT_LEAST_ONE_GROUP", bool), True)

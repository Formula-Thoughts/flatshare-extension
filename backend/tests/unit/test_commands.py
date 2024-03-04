import uuid
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call
from uuid import UUID

from autofixture import AutoFixture
from callee import Captor
from ddt import ddt, data
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper
from formula_thoughts_web.events import SQSEventPublisher, EVENT
from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups, CreateFlatRequest, Flat
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID, USER_BELONGS_TO_AT_LEAST_ONE_GROUP, USER_GROUPS, \
    CREATE_FLAT_REQUEST, GROUP, CODE
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, \
    UpdateGroupAsyncCommand, UpsertGroupBackgroundCommand, UpsertUserGroupsBackgroundCommand, \
    CreateUserGroupsAsyncCommand, FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, \
    ValidateIfGroupBelongsToUser, FetchGroupByIdCommand, SetFlatRequestCommand, CreateFlatCommand, \
    ValidateFlatRequestCommand, DeleteFlatCommand, AddCurrentUserToGroupCommand, SetGroupIdFromCodeCommand, \
    GetCodeFromGroupIdCommand, ValidateUserIsNotParticipantCommand, CreateGroupAsyncCommand
from src.domain.errors import invalid_price_error, UserGroupsNotFoundError, GroupNotFoundError, \
    invalid_group_locations_error, FlatNotFoundError, \
    current_user_already_added_to_group, code_required_error, user_already_part_of_group_error, \
    flat_price_required_error, flat_url_required_error, flat_location_required_error, group_price_limt_required_error
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse, GetGroupCodeResponse
from src.exceptions import UserGroupsNotFoundException, GroupNotFoundException

UUID_EXAMPLE = "723f9ec2-fec1-4616-9cf2-576ee632822d"


class TestSetGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetGroupRequestCommand(object_mapper=ObjectMapper(), logger=Mock())

    def test_run(self):
        # arrange
        locations = ["UK"]
        price_limit = 14.2
        context = ApplicationContext(variables={},
                                     body={"price_limit": price_limit, "locations": locations})

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="group request is set"):
            create_group_request = context.get_var("upsert_group_request", UpsertGroupRequest)
            self.assertEqual(create_group_request.locations, locations)
            self.assertEqual(create_group_request.price_limit, price_limit)


@ddt
class TestValidateGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateGroupCommand()

    def test_run_with_valid_data(self):
        # arrange
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=14.4, locations=["UK"])
        })

        # act
        self.__sut.run(context)

        # assert
        self.assertEqual(context.error_capsules, [])

    @data(
        [0, ["UK"], 1, invalid_price_error],
        [-14, ["UK"], 1, invalid_price_error],
        [54, [], 1, invalid_group_locations_error],
        [None, ["UK"], 1, group_price_limt_required_error],
        [0, [], 2, invalid_price_error])
    def test_run_with_invalid_data(self, data):
        # arrange
        [price_limit, locations, errors_count, error] = data
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=price_limit, locations=locations)
        })

        # act
        self.__sut.run(context)

        # assert
        with self.subTest(msg="assert 1 error capsule is added"):
            self.assertEqual(len(context.error_capsules), errors_count)

        # assert
        with self.subTest(msg="asser price error capsule is added"):
            self.assertEqual(context.error_capsules[0], error)


class TestSaveGroupAsyncOverSQSCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = UpdateGroupAsyncCommand(sqs_event_publisher=self.__sqs_event_publisher)

    def test_run_should_publish_to_sqs(self) -> None:
        # arrange
        group = AutoFixture().create(dto=Group)
        group_request = AutoFixture().create(dto=UpsertGroupRequest)
        auth_user_id = "12345"
        expected_group = Group(id=group.id,
                               price_limit=group_request.price_limit,
                               locations=group_request.locations,
                               flats=group.flats,
                               participants=group.participants)
        context = ApplicationContext(variables={
            GROUP: group,
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
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=group.id,
                                                                           payload=expected_group)

        # assert
        with self.subTest(msg="assert response is set to group"):
            self.assertEqual(SingleGroupResponse(group=expected_group), context.response)


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
        context = ApplicationContext(variables={GROUP_ID: group_id, USER_BELONGS_TO_AT_LEAST_ONE_GROUP: False},
                                     auth_user_id=auth_user_id)
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

    def test_run_should_modify_existing_user_groups_if_user_already_has_group(self) -> None:
        # arrange
        group_id = str(uuid.uuid4())
        auth_user_id = "12345"
        user_groups = AutoFixture().create(dto=UserGroups)
        expected_user_groups = user_groups.groups + [group_id]
        context = ApplicationContext(variables={
            GROUP_ID: group_id,
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: True,
            USER_GROUPS: user_groups
        },
                                     auth_user_id=auth_user_id)
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert sqs message is sent with correct params"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=auth_user_id,
                                                                           payload=UserGroups(auth_user_id=auth_user_id,
                                                                                              groups=expected_user_groups))


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
            self.assertEqual(context.get_var("user_groups", list[Group]), groups)

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
        context = ApplicationContext(auth_user_id=auth_user_id, variables={})
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
            self.assertEqual(context.get_var("user_groups", UserGroups), user_groups)

        # assert
        with self.subTest("validation result is set as context var"):
            self.assertEqual(context.get_var("user_belongs_to_at_least_one_group", bool), True)

    def test_run_when_user_has_no_groups(self):
        # arrange
        auth_user_id = "1235"
        context = ApplicationContext(auth_user_id=auth_user_id, variables={})
        self.__user_groups_repo.get = MagicMock(side_effect=UserGroupsNotFoundException())

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest("validation result is set as context var"):
            self.assertEqual(context.get_var(USER_BELONGS_TO_AT_LEAST_ONE_GROUP, bool), False)


class TestValidateIfGroupBelongsToUser(TestCase):

    def setUp(self):
        self.__sut = ValidateIfGroupBelongsToUser()

    def test_run_if_group_belongs_to_user(self):
        # arrange
        user_groups = AutoFixture().create(UserGroups)
        user_groups.groups = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
        group_id = user_groups.groups[0]
        context = ApplicationContext(variables={
            "group_id": group_id,
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: True,
            USER_GROUPS: user_groups
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert no errors are raised"):
            self.assertEqual(len(context.error_capsules), 0)

    def test_run_if_user_has_no_groups(self):
        # arrange
        group_id = "12345"
        context = ApplicationContext(variables={
            "group_id": group_id,
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: False
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert 1 error raised"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="assert user groups not found error is raised"):
            self.assertEqual(type(context.error_capsules[0]), UserGroupsNotFoundError)

    def test_run_if_user_has_groups_but_group_id_does_not_belong(self):
        # arrange
        user_groups = AutoFixture().create(UserGroups)
        user_groups.groups = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
        context = ApplicationContext(variables={
            "group_id": "1234",
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: True,
            USER_GROUPS: user_groups
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert 1 error raised"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="assert group not found error is raised"):
            self.assertEqual(type(context.error_capsules[0]), GroupNotFoundError)


class TestFetchGroupByIdCommand(TestCase):

    def setUp(self):
        self.__group_repo: IGroupRepo = Mock()
        self.__sut = FetchGroupByIdCommand(group_repo=self.__group_repo)

    def test_run(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        group_id = "1234"
        context = ApplicationContext(variables={GROUP_ID: group_id})
        self.__group_repo.get = MagicMock(return_value=group)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert repo was called once"):
            self.__group_repo.get.assert_called_once()

        # assert
        with self.subTest(msg="assert repo was called with correct params"):
            self.__group_repo.get.assert_called_with(_id=group_id)

        # assert
        with self.subTest(msg="group was set as context var"):
            self.assertEqual(context.get_var(name="group", _type=Group), group)

        # assert
        with self.subTest(msg="group was set as response"):
            self.assertEqual(context.response, SingleGroupResponse(group=group))

    def test_run_if_group_not_found(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        group_id = "1234"
        context = ApplicationContext(variables={GROUP_ID: group_id})
        self.__group_repo.get = MagicMock(side_effect=GroupNotFoundException())

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="single error was added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="group was set as response"):
            self.assertEqual(type(context.error_capsules[0]), GroupNotFoundError)


class TestSetFlatRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetFlatRequestCommand(object_mapper=ObjectMapper(), logger=Mock())

    def test_run(self):
        # arrange
        flat_request = AutoFixture().create(dto=CreateFlatRequest)
        context = ApplicationContext(body=flat_request.__dict__, variables={})

        # act
        self.__sut.run(context=context)

        # assert
        self.assertEqual(context.get_var(name="create_flat_request", _type=CreateFlatRequest), flat_request)


class TestCreateFlatCommand(TestCase):

    def setUp(self):
        self.__sqs_message_publisher: SQSEventPublisher = Mock()
        self.__sut = CreateFlatCommand(sqs_message_publisher=self.__sqs_message_publisher)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    def test_run(self, _):
        # arrange
        group = AutoFixture().create(dto=Group)
        flat = AutoFixture().create(dto=CreateFlatRequest)
        flats = AutoFixture().create_many(dto=Flat, ammount=3)
        group.flats = flats
        context = ApplicationContext(variables={
            CREATE_FLAT_REQUEST: flat,
            GROUP: group
        })
        self.__sqs_message_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)
        captor = Captor()

        # assert
        with self.subTest(msg="sqs bus is called once"):
            self.__sqs_message_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="sqs bus is called with valid params"):
            self.__sqs_message_publisher.send_sqs_message.assert_called_with(message_group_id=group.id, payload=captor)

        # assert
        with self.subTest(msg="response is set to updated group"):
            self.assertEqual(context.response, SingleGroupResponse(group=group))

        # assert
        with self.subTest(msg="correct number of flats are sent"):
            self.assertEqual(len(captor.arg.flats), 4)

        # assert
        with self.subTest(msg="correct flat params are set"):
            self.assertEqual(captor.arg.flats[-1], Flat(id=UUID_EXAMPLE, url=flat.url, price=flat.price, location=flat.location))


@ddt
class TestValidateFlatRequestCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateFlatRequestCommand()

    def test_run_when_valid(self):
        # arrange
        flat_request = AutoFixture().create(dto=CreateFlatRequest)
        context = ApplicationContext(variables={
            CREATE_FLAT_REQUEST: flat_request
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="no errors occur"):
            self.assertEqual(len(context.error_capsules), 0)

    @data(
        [None, "https://test.com", "UK", 1, flat_price_required_error],
        [100.20, None, "UK", 1, flat_url_required_error],
        [100.20, "https://test.com", None, 1, flat_location_required_error],
        [-10, "https://test.com", "UK", 1, invalid_price_error],
        [None, "https://test.com", None, 2, flat_price_required_error],
        [None, None, None, 3, flat_price_required_error])
    def test_run_when_invalid(self, data):
        # arrange
        [price, url, location, errors_count, error] = data
        context = ApplicationContext(variables={
            CREATE_FLAT_REQUEST: CreateFlatRequest(price=price, url=url, location=location)
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert error count is correct"):
            self.assertEqual(len(context.error_capsules), errors_count)

        # assert
        with self.subTest(msg="assert error is correct"):
            self.assertEqual(context.error_capsules[0], error)


class TestDeleteFlatCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = DeleteFlatCommand(sqs_event_publisher=self.__sqs_event_publisher)

    def test_run(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        flat = AutoFixture().create(dto=Flat)
        group.flats.append(flat)
        length_of_flats_before_delete = len(group.flats)
        context = ApplicationContext(variables={
            "flat_id": flat.id,
            GROUP: group
        })
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        captor = Captor()

        # assert
        with self.subTest(msg="assert sqs is called once"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="assert sqs is called with correct args"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=group.id,
                                                                           payload=captor)

        # assert
        with self.subTest(msg="assert flat is removed from list"):
            self.assertEqual(len(captor.arg.flats), length_of_flats_before_delete - 1)

        # assert
        with self.subTest(msg="assert group published matches"):
            self.assertEqual(captor.arg, group)

        # assert
        with self.subTest(msg="assert response is set"):
            self.assertEqual(context.response, SingleGroupResponse(group=group))

    def test_run_when_flat_is_not_found(self):
        # arrange
        group = AutoFixture().create(dto=Group)
        flat = AutoFixture().create(dto=Flat)
        context = ApplicationContext(variables={
            "flat_id": flat.id,
            GROUP: group
        })
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert sqs is never called"):
            self.__sqs_event_publisher.send_sqs_message.assert_not_called()

        # assert
        with self.subTest(msg="assert 1 error is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="assert flat not found error is added"):
            self.assertEqual(type(context.error_capsules[0]), FlatNotFoundError)


class TestAddCurrentUserToGroupCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = AddCurrentUserToGroupCommand(sqs_event_publisher=self.__sqs_event_publisher)

    def test_run(self):
        # arrange
        auth_user_id = "1234"
        group = AutoFixture().create(dto=Group)
        length_of_flats_before_delete = len(group.participants)
        context = ApplicationContext(variables={
            GROUP: group
        }, auth_user_id=auth_user_id)
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        captor = Captor()

        # assert
        with self.subTest(msg="assert sqs is called once"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="assert sqs is called with correct args"):
            self.__sqs_event_publisher.send_sqs_message.assert_called_with(message_group_id=group.id,
                                                                           payload=captor)

        # assert
        with self.subTest(msg="assert user is added to group"):
            self.assertEqual(len(captor.arg.participants), length_of_flats_before_delete + 1)

        # assert
        with self.subTest(msg="assert group published matches"):
            self.assertEqual(captor.arg, group)

        # assert
        with self.subTest(msg="assert response is set"):
            self.assertEqual(context.response, SingleGroupResponse(group=group))

    def test_run_when_user_is_already_in_the_group(self):
        # arrange
        auth_user_id = "1234"
        group = AutoFixture().create(dto=Group)
        group.participants.append(auth_user_id)
        context = ApplicationContext(variables={
            GROUP: group
        }, auth_user_id=auth_user_id)
        self.__sqs_event_publisher.send_sqs_message = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert sqs is never called"):
            self.__sqs_event_publisher.send_sqs_message.assert_not_called()

        # assert
        with self.subTest(msg="assert error is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="assert user already added error is added"):
            self.assertEqual(context.error_capsules[0], current_user_already_added_to_group)


class TestSetGroupIdFromCodeCommand(TestCase):

    def setUp(self):
        self.__sut = SetGroupIdFromCodeCommand()

    def test_run_when_code_provided(self):
        # arrange
        group_id = "b9a5865b-881c-493a-b237-44f96b8820bf"
        context = ApplicationContext(variables={
            "code": "YjlhNTg2NWItODgxYy00OTNhLWIyMzctNDRmOTZiODgyMGJm"
        })

        # act
        self.__sut.run(context=context)

        # assert
        self.assertEqual(context.get_var(name=GROUP_ID, _type=str), group_id)

    def test_run_when_code_not_provided(self):
        # arrange
        context = ApplicationContext(variables={})

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert 1 error is added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="assert code required error is added"):
            self.assertEqual(context.error_capsules[0], code_required_error)


class TestGetCodeFromGroupIdCommand(TestCase):

    def setUp(self):
        self.__sut = GetCodeFromGroupIdCommand()

    def test_run_when_code_provided(self):
        # arrange
        code = "YjlhNTg2NWItODgxYy00OTNhLWIyMzctNDRmOTZiODgyMGJm"
        context = ApplicationContext(variables={
            GROUP_ID: "b9a5865b-881c-493a-b237-44f96b8820bf"
        })

        # act
        self.__sut.run(context=context)

        # assert
        self.assertEqual(context.response, GetGroupCodeResponse(code=code))


class TestValidateUserIsNotParticipantCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateUserIsNotParticipantCommand()

    def test_run_when_user_is_not_part_of_group(self):
        # arrange
        auth_id = "1234"
        group = AutoFixture().create(dto=Group)
        context = ApplicationContext(variables={
            GROUP: group
        }, auth_user_id=auth_id)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="no errors added"):
            self.assertEqual(len(context.error_capsules), 0)

        # assert
        with self.subTest(msg="assert validation var is set"):
            self.assertEqual(context.get_var(name=USER_BELONGS_TO_AT_LEAST_ONE_GROUP, _type=bool), False)

    def test_run_when_user_is_already_part_of_group(self):
        # arrange
        auth_id = "1234"
        group = AutoFixture().create(dto=Group)
        group.participants.append(auth_id)
        context = ApplicationContext(variables={
            GROUP: group
        }, auth_user_id=auth_id)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="1 error added"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="1 error added"):
            self.assertEqual(context.error_capsules[0], user_already_part_of_group_error)


class TestCreateGroupAsyncCommand(TestCase):

    def setUp(self):
        self.__sqs_publisher: SQSEventPublisher = Mock()
        self.__sut = CreateGroupAsyncCommand(sqs_publisher=self.__sqs_publisher)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    def test_run(self, _):
        # arrange
        auth_user_id = "12345"
        context = ApplicationContext(auth_user_id=auth_user_id, variables={})
        self.__sqs_publisher.send_sqs_message = MagicMock()
        expected_group = Group(
                             id=UUID_EXAMPLE,
                             flats=[],
                             participants=[auth_user_id],
                             price_limit=None,
                             locations=[]
                         )

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert upsert group event was published once"):
            self.__sqs_publisher.send_sqs_message.assert_called_once()

        # assert
        with self.subTest(msg="assert upsert group event was published with correct params"):
            self.__sqs_publisher.send_sqs_message.assert_called_with(message_group_id=UUID_EXAMPLE,
                                                                     payload=expected_group)

        with self.subTest(msg="assert response was set to group"):
            self.assertEqual(context.response, CreatedGroupResponse(group=expected_group))

        with self.subTest(msg="assert group id var was set"):
            self.assertEqual(context.get_var(name=GROUP_ID, _type=str), UUID_EXAMPLE)
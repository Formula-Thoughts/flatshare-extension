import os
import uuid
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call
from uuid import UUID

from autofixture import AutoFixture
from callee import Captor
from ddt import ddt, data
from formula_thoughts_web.abstractions import ApplicationContext
from formula_thoughts_web.crosscutting import ObjectMapper
from formula_thoughts_web.events import SQSEventPublisher, EVENT

from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups, CreatePropertyRequest, \
    Property, GroupProperties, IPropertyRepo
from src.data import CognitoClientWrapper
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID, USER_BELONGS_TO_AT_LEAST_ONE_GROUP, USER_GROUPS, \
    CREATE_PROPERTY_REQUEST, GROUP, FULLNAME_CLAIM, PROPERTY_ID
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, \
    UpdateGroupAsyncCommand, UpsertGroupBackgroundCommand, UpsertUserGroupsBackgroundCommand, \
    CreateUserGroupsAsyncCommand, FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, \
    ValidateIfGroupBelongsToUserCommand, FetchGroupByIdCommand, SetPropertyRequestCommand, CreatePropertyCommand, \
    ValidatePropertyRequestCommand, DeletePropertyCommand, AddCurrentUserToGroupCommand, SetGroupIdFromCodeCommand, \
    GetCodeFromGroupIdCommand, ValidateUserIsNotParticipantCommand, CreateGroupAsyncCommand, \
    FetchAuthUserClaimsIfUserDoesNotExistCommand, CreateGroupCommand, CreateUserGroupsCommand, UpdateGroupCommand
from src.domain.errors import invalid_price_error, UserGroupsNotFoundError, GroupNotFoundError, \
    PropertyNotFoundError, \
    code_required_error, user_already_part_of_group_error, \
    property_price_required_error, property_url_required_error, property_title_required_error
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse, \
    GetGroupCodeResponse, SingleGroupPropertiesResponse, PropertyCreatedResponse
from src.exceptions import UserGroupsNotFoundException, GroupNotFoundException, PropertyNotFoundException

UUID_EXAMPLE = "723f9ec2-fec1-4616-9cf2-576ee632822d"
USER_POOL = "test_user_pool"


class TestSetGroupRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetGroupRequestCommand(object_mapper=ObjectMapper(), logger=Mock())

    def test_run(self):
        # arrange
        locations = ["UK"]
        price_limit = Decimal('14.2')
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

    @data(
        [None, ["UK"]],
        [None, []],
        [14, ["UK"]])
    def test_run_with_valid_data(self, data):
        # arrange
        [price_limit, locations] = data
        # arrange
        context = ApplicationContext(variables={
            UPSERT_GROUP_REQUEST: UpsertGroupRequest(price_limit=price_limit, locations=locations)
        })

        # act
        self.__sut.run(context)

        # assert
        self.assertEqual(context.error_capsules, [])

    @data(
        [0, ["UK"], 1, invalid_price_error],
        [-14, ["UK"], 1, invalid_price_error],
        [0, [], 1, invalid_price_error])
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
        name = "test_user"
        expected_user_group = UserGroups(id=auth_user_id,
                                         groups=[group_id],
                                         name=name)
        context = ApplicationContext(variables={
            GROUP_ID: group_id,
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: False,
            FULLNAME_CLAIM: name
        }, auth_user_id=auth_user_id)
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

        # assert
        with self.subTest(msg="assert user groups var is set"):
            self.assertEqual(context.get_var(name=USER_GROUPS, _type=UserGroups), expected_user_group)

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
                                                                           payload=UserGroups(id=auth_user_id,
                                                                                              groups=expected_user_groups,
                                                                                              name=user_groups.name))


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
            self.assertEqual(context.response, ListUserGroupsResponse(group_properties_list=groups))

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
        self.__sut = ValidateIfGroupBelongsToUserCommand()

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
        group = AutoFixture().create(dto=GroupProperties)
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
            self.assertEqual(context.response, SingleGroupPropertiesResponse(group_properties=group))

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


class TestSetPropertyRequestCommand(TestCase):

    def setUp(self):
        self.__sut = SetPropertyRequestCommand(object_mapper=ObjectMapper(), logger=Mock())

    def test_run(self):
        # arrange
        property_request = AutoFixture().create(dto=CreatePropertyRequest)
        context = ApplicationContext(body=property_request.__dict__, variables={})

        # act
        self.__sut.run(context=context)

        # assert
        self.assertEqual(context.get_var(name="create_property_request", _type=CreatePropertyRequest), property_request)


class TestCreatePropertyCommand(TestCase):

    def setUp(self):
        self.__property_repo: IPropertyRepo = Mock()
        self.__sut = CreatePropertyCommand(property_repo=self.__property_repo)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    def test_run(self, _):
        # arrange
        group = AutoFixture().create(dto=Group)
        user_groups = AutoFixture().create(dto=UserGroups)
        property = AutoFixture().create(dto=CreatePropertyRequest)
        context = ApplicationContext(variables={
            CREATE_PROPERTY_REQUEST: property,
            GROUP: group,
            USER_GROUPS: user_groups
        })
        expected_property = Property(url=property.url,
                                     title=property.title,
                                     price=property.price,
                                     full_name=user_groups.name)
        self.__property_repo.create = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="property is created once"):
            self.__property_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="property is created with correct property"):
            self.__property_repo.create.assert_called_with(group_id=group.id, property=expected_property)

        # assert
        with self.subTest(msg="response is set to updated group"):
            self.assertEqual(context.response, PropertyCreatedResponse(property=expected_property))

@ddt
class TestValidatePropertyRequestCommand(TestCase):

    def setUp(self):
        self.__sut = ValidatePropertyRequestCommand()

    def test_run_when_valid(self):
        # arrange
        property_request = AutoFixture().create(dto=CreatePropertyRequest)
        context = ApplicationContext(variables={
            CREATE_PROPERTY_REQUEST: property_request
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="no errors occur"):
            self.assertEqual(len(context.error_capsules), 0)

    @data(
        [None, "https://test.com", "UK", 1, property_price_required_error],
        [100.20, None, "UK", 1, property_url_required_error],
        [100.20, "https://test.com", None, 1, property_title_required_error],
        [-10, "https://test.com", "UK", 1, invalid_price_error],
        [None, "https://test.com", None, 2, property_price_required_error],
        [None, None, None, 3, property_price_required_error])
    def test_run_when_invalid(self, data):
        # arrange
        [price, url, location, errors_count, error] = data
        context = ApplicationContext(variables={
            CREATE_PROPERTY_REQUEST: CreatePropertyRequest(price=price, url=url, title=location)
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert error count is correct"):
            self.assertEqual(len(context.error_capsules), errors_count)

        # assert
        with self.subTest(msg="assert error is correct"):
            self.assertEqual(context.error_capsules[0], error)


class TestAddCurrentUserToGroupCommand(TestCase):

    def setUp(self):
        self.__sqs_event_publisher: SQSEventPublisher = Mock()
        self.__sut = AddCurrentUserToGroupCommand(sqs_event_publisher=self.__sqs_event_publisher)

    def test_run(self):
        # arrange
        fullname = "full name"
        group = AutoFixture().create(dto=Group)
        length_of_properties_before_delete = len(group.participants)
        context = ApplicationContext(variables={
            GROUP: group,
            FULLNAME_CLAIM: fullname
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
        with self.subTest(msg="assert user is append to group"):
            self.assertEqual(len(captor.arg.participants), length_of_properties_before_delete + 1)

        # assert
        with self.subTest(msg="assert correct user is added to group"):
            self.assertEqual(captor.arg.participants[-1], fullname)

        # assert
        with self.subTest(msg="assert group published matches"):
            self.assertEqual(captor.arg, group)

        # assert
        with self.subTest(msg="assert response is set"):
            self.assertEqual(context.response, SingleGroupResponse(group=group))


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
        fullname = "fullname"
        group = AutoFixture().create(dto=Group)
        context = ApplicationContext(variables={
            GROUP: group,
            FULLNAME_CLAIM: fullname
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="no errors added"):
            self.assertEqual(len(context.error_capsules), 0)

    def test_run_when_user_is_already_part_of_group(self):
        # arrange
        fullname = "fullname"
        group = AutoFixture().create(dto=Group)
        group.participants.append(fullname)
        context = ApplicationContext(variables={
            GROUP: group,
            FULLNAME_CLAIM: fullname
        })

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
        fullname = "full name"
        context = ApplicationContext(variables={
            FULLNAME_CLAIM: fullname
        })
        self.__sqs_publisher.send_sqs_message = MagicMock()
        expected_group = Group(
            id=UUID_EXAMPLE,
            participants=[fullname],
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


class TestFetchAuthUserClaimsCommand(TestCase):

    def setUp(self):
        self.__cognito_wrapper: CognitoClientWrapper = Mock()
        self.__sut = FetchAuthUserClaimsIfUserDoesNotExistCommand(cognito_wrapper=self.__cognito_wrapper)

    @patch.dict(os.environ, {"USER_POOL_ID": USER_POOL})
    def test_run_should_fetch_name_and_set_it(self):
        # arrange
        name = "test user"
        auth_user_id = "1234"
        context = ApplicationContext(variables={
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: False
        }, auth_user_id=auth_user_id)
        self.__cognito_wrapper.admin_get_user = MagicMock(return_value={
            'UserAttributes': [
                {
                    'Name': 'name',
                    'Value': name
                },
            ]
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert cognito was called once"):
            self.__cognito_wrapper.admin_get_user.assert_called_once()

        # assert
        with self.subTest(msg="assert cogntio was called with correct params"):
            self.__cognito_wrapper.admin_get_user.assert_called_with(user_pool_id=USER_POOL, username=auth_user_id)

        # assert
        with self.subTest(msg="assert full name was set as var"):
            self.assertEqual(context.get_var("fullname_claim", str), name)

    @patch.dict(os.environ, {"USER_POOL_ID": USER_POOL})
    def test_run_should_not_fetch_if_user_groups_already_exists(self):
        # arrange
        user_groups = AutoFixture().create(dto=UserGroups)
        context = ApplicationContext(variables={
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: True,
            USER_GROUPS: user_groups
        })
        self.__cognito_wrapper.admin_get_user = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="cognito is not called"):
            self.__cognito_wrapper.admin_get_user.assert_not_called()

        # assert
        with self.subTest(msg="assert full name was set as var"):
            self.assertEqual(context.get_var(FULLNAME_CLAIM, str), user_groups.name)


class TestCreateGroupCommand(TestCase):

    def setUp(self):
        self.__group_repo: IGroupRepo = Mock()
        self.__sut = CreateGroupCommand(group_repo=self.__group_repo)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    def test_run(self, _):
        # arrange
        gannon = "aidan gannon"
        context = ApplicationContext(variables={
            FULLNAME_CLAIM: gannon
        })
        self.__group_repo.create = MagicMock()
        expected_group = Group(id=UUID_EXAMPLE, participants=[gannon])

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert group is created once"):
            self.__group_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="assert group is created with correct args"):
            self.__group_repo.create.assert_called_with(group=expected_group)

        # assert
        with self.subTest(msg="assert group response is returned"):
            self.assertEqual(context.response, CreatedGroupResponse(group=expected_group))

        # assert
        with self.subTest(msg="assert group id var is set"):
            self.assertEqual(context.get_var(name=GROUP_ID, _type=str), UUID_EXAMPLE)


class TestCreateUserGroupsCommand(TestCase):

    def setUp(self):
        self.__user_groups_repo: IUserGroupsRepo = Mock()
        self.__sut = CreateUserGroupsCommand(user_groups_repo=self.__user_groups_repo)

    def test_run_when_user_groups_does_not_exist(self):
        # arrange
        self.__user_groups_repo.create = MagicMock()
        gannon = "aidan gannon"
        auth_user_id = "1234"
        group_id = "group_id"
        context = ApplicationContext(variables={
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: False,
            FULLNAME_CLAIM: gannon,
            GROUP_ID: group_id
        }, auth_user_id=auth_user_id)
        expected_user_groups = UserGroups(id=auth_user_id,
                                          name=gannon,
                                          groups=[group_id])

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="user group is created once"):
            self.__user_groups_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="user group is created with correct fields"):
            self.__user_groups_repo.create.assert_called_with(user_groups=expected_user_groups)

        # assert
        with self.subTest(msg="user groups var is set"):
            self.assertEqual(expected_user_groups, context.get_var(name=USER_GROUPS, _type=UserGroups))

    def test_run_when_user_groups_exists(self):
        # arrange
        self.__user_groups_repo.create = MagicMock()
        self.__user_groups_repo.add_group = MagicMock()
        gannon = "aidan gannon"
        auth_user_id = "1234"
        group_id = "group_id"
        user_groups = AutoFixture().create(dto=UserGroups)
        context = ApplicationContext(variables={
            USER_BELONGS_TO_AT_LEAST_ONE_GROUP: True,
            FULLNAME_CLAIM: gannon,
            GROUP_ID: group_id,
            USER_GROUPS: user_groups
        }, auth_user_id=auth_user_id)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="user group is not created"):
            self.__user_groups_repo.create.assert_not_called()

        # assert
        with self.subTest(msg="group is added once"):
            self.__user_groups_repo.add_group.assert_called_once()

        # assert
        with self.subTest(msg="correct group is added"):
            self.__user_groups_repo.add_group.assert_called_with(user_groups=user_groups, group=group_id)


class TestUpdateGroupCommand(TestCase):

    def setUp(self):
        self.__group_repo: IGroupRepo = Mock()
        self.__sut = UpdateGroupCommand(group_repo=self.__group_repo)

    def test_update(self):
        # arrange
        self.__group_repo.update = MagicMock()
        group_properties = AutoFixture().create(dto=GroupProperties)
        group_request = AutoFixture().create(dto=UpsertGroupRequest)
        context = ApplicationContext(variables={
            GROUP: group_properties,
            UPSERT_GROUP_REQUEST: group_request
        })
        expected_group_from_update = Group(id=group_properties.id,
                                           etag=group_properties.etag,
                                           partition_key=group_properties.partition_key,
                                           participants=group_properties.participants,
                                           price_limit=group_request.price_limit,
                                           locations=group_request.locations)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="group was updated once"):
            self.__group_repo.update.assert_called_once()

        # assert
        with self.subTest(msg="group was updated with correct group"):
            self.__group_repo.update.assert_called_with(group=expected_group_from_update)

        # assert
        with self.subTest(msg="group response is set"):
            self.assertEqual(context.response, SingleGroupResponse(group=expected_group_from_update))


class TestDeletePropertyCommand(TestCase):

    def setUp(self):
        self.__property_repo: IPropertyRepo = Mock()
        self.__sut = DeletePropertyCommand(property_repo=self.__property_repo)

    def test_run(self):
        # arrange
        property_id = str(uuid.uuid4())
        group = AutoFixture().create(dto=Group)
        context = ApplicationContext(variables={
            GROUP: group,
            "property_id": property_id
        })
        self.__property_repo.delete = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="property was deleted once"):
            self.__property_repo.delete.assert_called_once()

        # assert
        with self.subTest(msg="property was deleted with correct property"):
            self.__property_repo.delete.assert_called_with(group_id=group.id, property_id=property_id)

        # assert
        with self.subTest(msg="response is set to empty"):
            self.assertEqual(context.response, None)

    def test_run_when_property_is_not_found(self):
        # arrange
        property_id = str(uuid.uuid4())
        group = AutoFixture().create(dto=Group)
        context = ApplicationContext(variables={
            GROUP: group,
            PROPERTY_ID: property_id
        })
        self.__property_repo.delete = Mock()
        self.__property_repo.delete.side_effect = [PropertyNotFoundException()]

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="property not found error was added"):
            self.assertEqual(context.error_capsules[0], PropertyNotFoundError())
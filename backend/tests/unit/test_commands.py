import datetime
import os
import uuid
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call
from uuid import UUID

from autofixture import AutoFixture
from ddt import ddt, data
from formula_thoughts_web.abstractions import ApplicationContext, Error
from formula_thoughts_web.crosscutting import ObjectMapper

from src.core import UpsertGroupRequest, Group, IGroupRepo, IUserGroupsRepo, UserGroups, CreatePropertyRequest, \
    Property, GroupProperties, IPropertyRepo, IRedFlagRepo, CreateRedFlagRequest, RedFlag, AnonymousRedFlag
from src.data import CognitoClientWrapper
from src.domain import UPSERT_GROUP_REQUEST, GROUP_ID, USER_BELONGS_TO_AT_LEAST_ONE_GROUP, USER_GROUPS, \
    CREATE_PROPERTY_REQUEST, GROUP, FULLNAME_CLAIM, PROPERTY_ID, CREATE_RED_FLAG_REQUEST, RED_FLAG, PROPERTY_URL, \
    RED_FLAGS, RED_FLAG_ID
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, \
    FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, \
    ValidateIfGroupBelongsToUserCommand, FetchGroupByIdCommand, SetPropertyRequestCommand, CreatePropertyCommand, \
    ValidatePropertyRequestCommand, DeletePropertyCommand, AddCurrentUserToGroupCommand, SetGroupIdFromCodeCommand, \
    GetCodeFromGroupIdCommand, ValidateUserIsNotParticipantCommand, \
    FetchAuthUserClaimsIfUserDoesNotExistCommand, CreateGroupCommand, CreateUserGroupsCommand, UpdateGroupCommand, \
    CreateRedFlagCommand, SetRedFlagRequestCommand, ValidateRedFlagRequestCommand, SetCreatedAnonymousRedFlagCommand, \
    GetRedFlagsCommand, ValidatePropertyUrlCommand, SetAnonymousRedFlagsCommand, GetRedFlagByIdCommand, \
    SetAnonymousRedFlagCommand, ValidateAlreadyVotedCommand, ValidateNotVotedCommand, CreateVoteCommand
from src.domain.errors import invalid_price_error, UserGroupsNotFoundError, GroupNotFoundError, \
    PropertyNotFoundError, \
    code_required_error, user_already_part_of_group_error, \
    property_price_required_error, property_url_required_error, property_title_required_error, InvalidRedFlagDataError, \
    RedFlagNotFoundError, InvalidVotingStatusError
from src.domain.helpers import RedFlagMappingHelper
from src.domain.responses import CreatedGroupResponse, ListUserGroupsResponse, SingleGroupResponse, \
    GetGroupCodeResponse, SingleGroupPropertiesResponse, PropertyCreatedResponse, SingleRedFlagResponse, \
    CreatedRedFlagResponse, ListRedFlagsResponse
from src.exceptions import UserGroupsNotFoundException, GroupNotFoundException, PropertyNotFoundException, \
    RedFlagNotFoundException

UUID_EXAMPLE = "723f9ec2-fec1-4616-9cf2-576ee632822d"
UTC_NOW = datetime.datetime.fromisoformat("2024-07-04T11:09:39+00:00")
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
        self.__group_repo: IGroupRepo = Mock()
        self.__sut = AddCurrentUserToGroupCommand(group_repo=self.__group_repo)

    def test_run(self):
        # arrange
        fullname = "full name"
        group = AutoFixture().create(dto=GroupProperties)
        expected_group = Group(etag=group.etag,
                               id=group.id,
                               partition_key=group.partition_key,
                               participants=group.participants,
                               price_limit=group.price_limit,
                               locations=group.locations)
        context = ApplicationContext(variables={
            GROUP: group,
            FULLNAME_CLAIM: fullname
        })
        self.__group_repo.add_participant = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert add user is called once"):
            self.__group_repo.add_participant.assert_called_once()

        # assert
        with self.subTest(msg="assert add user is called with correct args"):
            self.__group_repo.add_participant.assert_called_with(participant=fullname,
                                                                 group=expected_group)

        # assert
        with self.subTest(msg="assert response is set"):
            self.assertEqual(context.response, SingleGroupResponse(group=expected_group))


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
            self.assertEqual(context.error_capsules[0], PropertyNotFoundError(message=f"property {property_id} for {group.id} not found"))


class TestCreateRedFlagCommand(TestCase):

    def setUp(self):
        self.__red_flag_repo: IRedFlagRepo = Mock()
        self.__sut = CreateRedFlagCommand(red_flag_repo=self.__red_flag_repo)

    @patch('uuid.uuid4', return_value=UUID(UUID_EXAMPLE))
    @patch('formula_thoughts_web.crosscutting.utc_now', return_value=UTC_NOW)
    def test_run(self, *_):
        # arrange
        create_red_flag_request = AutoFixture().create(dto=CreateRedFlagRequest)
        context = ApplicationContext(variables={
            CREATE_RED_FLAG_REQUEST: create_red_flag_request
        })
        self.__red_flag_repo.create = MagicMock()
        expected_red_flag = RedFlag(id=UUID_EXAMPLE,
                                    body=create_red_flag_request.body,
                                    property_url=create_red_flag_request.property_url,
                                    date=UTC_NOW)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="red flag is created once"):
            self.__red_flag_repo.create.assert_called_once()

        # assert
        with self.subTest(msg="correct red flag is created"):
            self.__red_flag_repo.create.assert_called_with(red_flag=expected_red_flag)

        # assert
        with self.subTest(msg="red flag variable is set"):
            self.assertEqual(context.get_var(name="red_flag", _type=RedFlag), expected_red_flag)


class TestSetRedFlagRequestCommand(TestCase):

    def setUp(self) -> None:
        self.__object_mapper = ObjectMapper()
        self.__sut = SetRedFlagRequestCommand(object_mapper=self.__object_mapper, logger=Mock())

    def test_run(self):
        # arrange
        create_red_flag_request = AutoFixture().create(dto=CreateRedFlagRequest)
        context = ApplicationContext(body=self.__object_mapper.map_to_dict(_from=create_red_flag_request,
                                                                           to=CreateRedFlagRequest),
                                     variables={})

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="red flag request is set"):
            self.assertEqual(context.get_var(name="create_red_flag_request", _type=CreateRedFlagRequest),
                             create_red_flag_request)


class TestValidateRedFlagRequestCommand(TestCase):

    def setUp(self) -> None:
        self.__sut = ValidateRedFlagRequestCommand()

    def test_run_when_valid(self):
        # arrange
        create_red_flag_request = AutoFixture().create(dto=CreateRedFlagRequest)
        context = ApplicationContext(variables={
            CREATE_RED_FLAG_REQUEST: create_red_flag_request
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="no errors are set"):
            self.assertEqual(len(context.error_capsules), 0)

    def test_run_when_url_is_missing(self):
        # arrange
        create_red_flag_request = AutoFixture().create(dto=CreateRedFlagRequest)
        create_red_flag_request.property_url = None
        context = ApplicationContext(variables={
            CREATE_RED_FLAG_REQUEST: create_red_flag_request
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="1 error is set"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="missing url error is set"):
            self.assertEqual(context.error_capsules[0], InvalidRedFlagDataError(message="property url field is a required attribute"))

    def test_run_when_body_is_missing(self):
        # arrange
        create_red_flag_request = AutoFixture().create(dto=CreateRedFlagRequest)
        create_red_flag_request.body = None
        context = ApplicationContext(variables={
            CREATE_RED_FLAG_REQUEST: create_red_flag_request
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="1 error is set"):
            self.assertEqual(len(context.error_capsules), 1)

        # assert
        with self.subTest(msg="missing body error is set"):
            self.assertEqual(context.error_capsules[0], InvalidRedFlagDataError(message="body field is a required attribute"))


class TestSetCreatedAnonymousRedFlagCommand(TestCase):

    def setUp(self):
        self.__red_flag_mapper: RedFlagMappingHelper = Mock()
        self.__sut = SetCreatedAnonymousRedFlagCommand(red_flag_mapping_helper=self.__red_flag_mapper)

    def test_run(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        anonymous_red_flag = AutoFixture().create(dto=AnonymousRedFlag)
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)
        self.__red_flag_mapper.map_to_anonymous = MagicMock(return_value=anonymous_red_flag)

        # act
        self.__sut.run(context=context)

        # arrange
        with self.subTest(msg="response is set to created red flag"):
            self.assertEqual(context.response, CreatedRedFlagResponse(red_flag=anonymous_red_flag))

        # arrange
        with self.subTest(msg="response is set to created red flag"):
            self.__red_flag_mapper.map_to_anonymous.assert_called_once()

        # arrange
        with self.subTest(msg="response is set to created red flag"):
            self.__red_flag_mapper.map_to_anonymous.assert_called_with(current_user=user, red_flag=red_flag)


class TestGetRedFlagsCommand(TestCase):

    def setUp(self):
        self.__red_flag_repo: IRedFlagRepo = Mock()
        self.__sut = GetRedFlagsCommand(red_flag_repo=self.__red_flag_repo)

    def test_run(self):
        # arrange
        property_url = "http://example.com"
        red_flags = AutoFixture().create_many(dto=RedFlag, ammount=5)
        self.__red_flag_repo.get_by_url = MagicMock(return_value=red_flags)
        context = ApplicationContext(variables={
            PROPERTY_URL: property_url
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert red flags are fetched once"):
            self.__red_flag_repo.get_by_url.assert_called_once()

        # assert
        with self.subTest(msg="assert red flags are fetched with correct property url"):
            self.__red_flag_repo.get_by_url.assert_called_with(property_url=property_url)

        # assert
        with self.subTest(msg="assert red flags are fetched with correct property url"):
            self.assertEqual(context.get_var(name=RED_FLAGS, _type=list[RedFlag]), red_flags)


class TestIValidatePropertyUrlCommand(TestCase):

    def setUp(self):
        self.__sut = ValidatePropertyUrlCommand()

    def test_run_when_property_is_set(self):
        # arrange
        property_url = "http://example.com"
        context = ApplicationContext(variables={
            "property_url": property_url
        })

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert no errors are set"):
            self.assertEqual(len(context.error_capsules), 0)

    def test_run_when_property_is_not_set(self):
        # arrange
        context = ApplicationContext(variables={})

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert property url is required error is set"):
            self.assertEqual(context.error_capsules, [InvalidRedFlagDataError("property url parameter is required")])


class TestSetAnonymousRedFlagsCommand(TestCase):

    def setUp(self):
        self.__red_flag_mapping_helper: RedFlagMappingHelper = Mock()
        self.__sut = SetAnonymousRedFlagsCommand(red_flag_mapping_helper=self.__red_flag_mapping_helper)

    def test_run(self):
        # arrange
        user = "1234"
        red_flags = AutoFixture().create_many(dto=RedFlag, ammount=5)
        anonymous_red_flags = AutoFixture().create_many(dto=AnonymousRedFlag, ammount=5)
        context = ApplicationContext(variables={
            RED_FLAGS: red_flags
        }, auth_user_id=user)
        self.__red_flag_mapping_helper.map_to_anonymous = Mock()
        self.__red_flag_mapping_helper.map_to_anonymous.side_effect = anonymous_red_flags

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert red flag mapper was called 5 times"):
            self.__red_flag_mapping_helper.map_to_anonymous.assert_has_calls([
                call(current_user=user, red_flag=red_flags[0]),
                call(current_user=user, red_flag=red_flags[1]),
                call(current_user=user, red_flag=red_flags[2]),
                call(current_user=user, red_flag=red_flags[3]),
                call(current_user=user, red_flag=red_flags[4])
            ])

        # assert
        with self.subTest(msg="assert red flags response was set"):
            self.assertEqual(context.response, ListRedFlagsResponse(red_flags=anonymous_red_flags))


class TestGetRedFlagByIdCommand(TestCase):

    def setUp(self):
        self.__red_flag_repo: IRedFlagRepo = Mock()
        self.__sut = GetRedFlagByIdCommand(red_flag_repo=self.__red_flag_repo)

    def test_run(self):
        # arrange
        red_flag_id = "123566"
        property_url = "https://www.reddit.com/r/"
        context = ApplicationContext(variables={
            "red_flag_id": red_flag_id,
            PROPERTY_URL: property_url
        })
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__red_flag_repo.get = MagicMock(return_value=red_flag)

        # act
        self.__sut.run(context=context)

        # arrange
        with self.subTest(msg="assert repo is called once"):
            self.__red_flag_repo.get.assert_called_once()

        # arrange
        with self.subTest(msg="assert repo is called once"):
            self.__red_flag_repo.get.assert_called_with(property_url=property_url, _id=red_flag_id)

        # arrange
        with self.subTest(msg="red flag variable is set"):
            self.assertEqual(context.get_var(name=RED_FLAG, _type=RedFlag), red_flag)

    def test_run_when_not_found(self):
        # arrange
        red_flag_id = "123566"
        property_url = "https://www.reddit.com/r/"
        context = ApplicationContext(variables={
            RED_FLAG_ID: red_flag_id,
            PROPERTY_URL: property_url
        })
        red_flag = AutoFixture().create(dto=RedFlag)
        self.__red_flag_repo.get = MagicMock(side_effect=RedFlagNotFoundException())

        # act
        self.__sut.run(context=context)

        # arrange
        with self.subTest(msg="red flag not found error is set"):
            self.assertEqual(context.error_capsules, [RedFlagNotFoundError(message=f"red flag {property_url}:{red_flag_id} not found")])


class TestSetAnonymousRedFlagCommand(TestCase):

    def setUp(self):
        self.__red_flag_mapping_helper = Mock()
        self.__sut = SetAnonymousRedFlagCommand(red_flag_mapping_helper=self.__red_flag_mapping_helper)

    def test_run(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        anonymous_red_flag = AutoFixture().create(dto=AnonymousRedFlag)
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)
        self.__red_flag_mapping_helper.map_to_anonymous = MagicMock(return_value=anonymous_red_flag)

        # act
        self.__sut.run(context=context)

        # arrange
        with self.subTest(msg="response is set to created red flag"):
            self.assertEqual(context.response, SingleRedFlagResponse(red_flag=anonymous_red_flag))

        # arrange
        with self.subTest(msg="response is set to created red flag"):
            self.__red_flag_mapping_helper.map_to_anonymous.assert_called_once()

        # arrange
        with self.subTest(msg="response is set to created red flag"):
            self.__red_flag_mapping_helper.map_to_anonymous.assert_called_with(current_user=user, red_flag=red_flag)


class TestValidateAlreadyVotedCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateAlreadyVotedCommand()

    def test_run_when_user_has_already_voted(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        red_flag.votes.append(user)
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert no error is added"):
            self.assertEqual(context.error_capsules, [])

    def test_run_when_user_has_not_already_voted(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert voting error is added"):
            self.assertEqual(context.error_capsules, [InvalidVotingStatusError(message="current user has not voted")])


class TestValidateNotVotedCommand(TestCase):

    def setUp(self):
        self.__sut = ValidateNotVotedCommand()

    def test_run_when_user_has_already_voted(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        red_flag.votes.append(user)
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert voting error is added"):
            self.assertEqual(context.error_capsules, [InvalidVotingStatusError(message="current user has already voted")])

    def test_run_when_user_has_not_already_voted(self):
        # arrange
        user = "1234"
        red_flag = AutoFixture().create(dto=RedFlag)
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="assert no error is added"):
            self.assertEqual(context.error_capsules, [])


class TestCreateVoteCommand(TestCase):

    def setUp(self):
        self.__red_flag_repo: IRedFlagRepo = Mock()
        self.__sut = CreateVoteCommand(red_flag_repo=self.__red_flag_repo)

    def test_run(self):
        # arrange
        red_flag = AutoFixture().create(dto=RedFlag)
        user = "12345"
        context = ApplicationContext(variables={
            RED_FLAG: red_flag
        }, auth_user_id=user)
        self.__red_flag_repo.add_voter = MagicMock()

        # act
        self.__sut.run(context=context)

        # assert
        with self.subTest(msg="red flag is upvoted once"):
            self.__red_flag_repo.add_voter.assert_called_once()

        # assert
        with self.subTest(msg="red flag is upvoted for user"):
            self.__red_flag_repo.add_voter.assert_called_with(user_id=user, red_flag=red_flag)

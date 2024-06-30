from unittest import TestCase
from unittest.mock import Mock

from src.core import IValidateGroupCommand, ISetGroupRequestCommand, IUpdateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IValidateIfUserBelongsToAtLeastOneGroupCommand, IValidateIfGroupBelongsToUser, \
    IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetPropertyRequestCommand, ICreatePropertyCommand, \
    IValidatePropertyRequestCommand, IDeletePropertyCommand, IAddCurrentUserToGroupCommand, ISetGroupIdFromCodeCommand, \
    IGetCodeFromGroupIdCommand, IValidateUserIsNotParticipantCommand, ICreateGroupAsyncCommand, \
    IFetchAuthUserClaimsIfUserDoesNotExistCommand, IFetchUserGroupIfExistsSequenceBuilder
from src.domain.sequence_builders import UpdateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder, \
    UpsertUserGroupsBackgroundSequenceBuilder, FetchUserGroupsSequenceBuilder, GetUserGroupByIdSequenceBuilder, \
    CreatePropertySequenceBuilder, DeletePropertySequenceBuilder, AddUserToGroupSequenceBuilder, GetCodeForGroupSequenceBuilder, \
    CreateGroupSequenceBuilder, FetchUserGroupIfExistsSequenceBuilder


class TestUpdateGroupAsyncSequenceBuilder(TestCase):

    def setUp(self):
        self.__save: IUpdateGroupAsyncCommand = Mock()
        self.__build_request: ISetGroupRequestCommand = Mock()
        self.__validate_request: IValidateGroupCommand = Mock()
        self.__validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUser = Mock()
        self.__validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand = Mock()
        self.__fetch_group_by_id: IFetchGroupByIdCommand = Mock()
        self.__sut = UpdateGroupSequenceBuilder(set_group_request=self.__build_request,
                                                validate_group=self.__validate_request,
                                                save_group_async=self.__save,
                                                validate_if_group_belongs_to_user=self.__validate_if_group_belongs_to_user,
                                                validate_if_user_belongs_to_at_least_one_group_command=self.__validate_if_user_belongs_to_at_least_one_group_command,
                                                fetch_group_by_id=self.__fetch_group_by_id)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__build_request,
                                                 self.__validate_request,
                                                 self.__validate_if_user_belongs_to_at_least_one_group_command,
                                                 self.__validate_if_group_belongs_to_user,
                                                 self.__fetch_group_by_id,
                                                 self.__save])


class TestUpsertGroupBackgroundSequenceBuilder(TestCase):

    def setUp(self):
        self.__upsert_background_command: IUpsertGroupBackgroundCommand = Mock()
        self.__sut = UpsertGroupBackgroundSequenceBuilder(upsert_background_command=self.__upsert_background_command)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__upsert_background_command])


class TestUpsertUserGroupsBackgroundSequenceBuilder(TestCase):

    def setUp(self):
        self.__upsert_background_command: IUpsertUserGroupsBackgroundCommand = Mock()
        self.__sut = UpsertUserGroupsBackgroundSequenceBuilder(
            upsert_background_command=self.__upsert_background_command)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__upsert_background_command])


class TestFetchUserGroupsSequenceBuilder(TestCase):

    def setUp(self):
        self.__fetch_user_groups_command: IFetchUserGroupsCommand = Mock()
        self.__sut = FetchUserGroupsSequenceBuilder(fetch_user_group_command=self.__fetch_user_groups_command)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__fetch_user_groups_command])


class TestGetUserGroupByIdSequenceBuilder(TestCase):

    def setUp(self):
        self.__validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand = Mock()
        self.__validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUser = Mock()
        self.__fetch_group_by_id_command: IFetchGroupByIdCommand = Mock()
        self.__sut = GetUserGroupByIdSequenceBuilder(
            validate_if_user_belongs_to_at_least_one_group_command=self.__validate_if_user_belongs_to_at_least_one_group_command,
            validate_if_group_belongs_to_user=self.__validate_if_group_belongs_to_user,
            fetch_group_by_id_command=self.__fetch_group_by_id_command)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__validate_if_user_belongs_to_at_least_one_group_command,
            self.__validate_if_group_belongs_to_user,
            self.__fetch_group_by_id_command
        ])


class TestCreatePropertySequenceBuilder(TestCase):

    def setUp(self):
        self.__get_user_group_by_id: IGetUserGroupByIdSequenceBuilder = Mock()
        self.__set_create_property_request: ISetPropertyRequestCommand = Mock()
        self.__create_property: ICreatePropertyCommand = Mock()
        self.__validate_property: IValidatePropertyRequestCommand = Mock()
        self.__sut = CreatePropertySequenceBuilder(get_user_group_by_id=self.__get_user_group_by_id,
                                               set_create_property_request=self.__set_create_property_request,
                                               create_property=self.__create_property,
                                               validate_property=self.__validate_property)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__set_create_property_request,
            self.__get_user_group_by_id,
            self.__validate_property,
            self.__create_property
        ])


class TestDeletePropertySequenceBuilder(TestCase):

    def setUp(self):
        self.__get_user_group_by_id: IGetUserGroupByIdSequenceBuilder = Mock()
        self.__delete_property: IDeletePropertyCommand = Mock()
        self.__sut = DeletePropertySequenceBuilder(get_user_group_by_id=self.__get_user_group_by_id,
                                               delete_property=self.__delete_property)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__get_user_group_by_id,
            self.__delete_property
        ])


class TestAddUserToGroupSequenceBuilder(TestCase):

    def setUp(self):
        self.__set_group_id_from_code: ISetGroupIdFromCodeCommand = Mock()
        self.__get_group_by_id: IFetchGroupByIdCommand = Mock()
        self.__add_current_user_to_group_command: IAddCurrentUserToGroupCommand = Mock()
        self.__validate_user_is_not_participant: IValidateUserIsNotParticipantCommand = Mock()
        self.__create_user_groups: ICreateUserGroupsAsyncCommand = Mock()
        self.__fetch_user_group_if_exists: IFetchUserGroupIfExistsSequenceBuilder = Mock()
        self.__sut = AddUserToGroupSequenceBuilder(get_group_by_id=self.__get_group_by_id,
                                                   add_current_user_to_group_command=self.__add_current_user_to_group_command,
                                                   set_group_id_from_code=self.__set_group_id_from_code,
                                                   validate_user_is_not_participant=self.__validate_user_is_not_participant,
                                                   create_user_groups=self.__create_user_groups,
                                                   fetch_user_group_if_exists=self.__fetch_user_group_if_exists)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__fetch_user_group_if_exists,
            self.__set_group_id_from_code,
            self.__get_group_by_id,
            self.__validate_user_is_not_participant,
            self.__add_current_user_to_group_command,
            self.__create_user_groups
        ])


class TestGetCodeForGroupSequenceBuilder(TestCase):

    def setUp(self):
        self.__get_code_from_group_id: IGetCodeFromGroupIdCommand = Mock()
        self.__get_group_by_id_sequence: IGetUserGroupByIdSequenceBuilder = Mock()
        self.__sut = GetCodeForGroupSequenceBuilder(get_code_from_group_id=self.__get_code_from_group_id,
                                                    get_group_by_id_sequence=self.__get_group_by_id_sequence)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__get_group_by_id_sequence,
            self.__get_code_from_group_id
        ])


class TestCreateGroupSequenceBuilder(TestCase):

    def setUp(self):
        self.__fetch_user_group_if_exists: IFetchUserGroupIfExistsSequenceBuilder = Mock()
        self.__create_user_groups: ICreateUserGroupsAsyncCommand = Mock()
        self.__create_group: ICreateGroupAsyncCommand = Mock()
        self.__sut = CreateGroupSequenceBuilder(
            fetch_user_group_if_exists=self.__fetch_user_group_if_exists,
            create_user_groups=self.__create_user_groups,
            create_group=self.__create_group)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__fetch_user_group_if_exists,
            self.__create_group,
            self.__create_user_groups
        ])


class TestFetchUserGroupIfExistsSequenceBuilder(TestCase):

    def setUp(self):
        self.__validate_user_belongs_to_one_group: IValidateIfUserBelongsToAtLeastOneGroupCommand = Mock()
        self.__fetch_auth_claims_if_user_has_no_group: IFetchAuthUserClaimsIfUserDoesNotExistCommand = Mock()
        self.__sut = FetchUserGroupIfExistsSequenceBuilder(
            validate_user_belongs_to_at_least_one_group=self.__validate_user_belongs_to_one_group,
            fetch_auth_claims_if_user_has_no_group=self.__fetch_auth_claims_if_user_has_no_group)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__validate_user_belongs_to_one_group,
            self.__fetch_auth_claims_if_user_has_no_group
        ])

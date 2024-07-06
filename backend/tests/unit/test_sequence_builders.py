from unittest import TestCase
from unittest.mock import Mock

from src.core import IFetchUserGroupsCommand, IValidateIfUserBelongsToAtLeastOneGroupCommand, \
    IValidateIfGroupBelongsToUserCommand, \
    IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetPropertyRequestCommand, ICreatePropertyCommand, \
    IValidatePropertyRequestCommand, IDeletePropertyCommand, IAddCurrentUserToGroupCommand, ISetGroupIdFromCodeCommand, \
    IGetCodeFromGroupIdCommand, IValidateUserIsNotParticipantCommand, \
    IFetchAuthUserClaimsIfUserDoesNotExistCommand, IFetchUserGroupIfExistsSequenceBuilder, ICreateUserGroupsCommand, \
    ICreateGroupCommand, ISetRedFlagRequestCommand, IValidateRedFlagRequestCommand, ICreateRedFlagCommand, \
    ISetCreatedAnonymousRedFlagCommand, IValidatePropertyUrlCommand, IGetRedFlagsCommand, \
    ISetAnonymousRedFlagsCommand, IGetRedFlagByIdCommand, ISetAnonymousRedFlagCommand, IValidateAlreadyVotedCommand
from src.domain.sequence_builders import FetchUserGroupsSequenceBuilder, \
    GetUserGroupByIdSequenceBuilder, \
    CreatePropertySequenceBuilder, DeletePropertySequenceBuilder, AddUserToGroupSequenceBuilder, \
    GetCodeForGroupSequenceBuilder, \
    CreateGroupSequenceBuilder, FetchUserGroupIfExistsSequenceBuilder, CreateRedFlagSequenceBuilder, \
    GetRedFlagsSequenceBuilder, CreateVoteForRedFlagSequenceBuilder, DeleteVoteForRedFlagSequenceBuilder


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
        self.__validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUserCommand = Mock()
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
        self.__create_user_groups: ICreateUserGroupsCommand = Mock()
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
        self.__create_user_groups: ICreateUserGroupsCommand = Mock()
        self.__create_group: ICreateGroupCommand = Mock()
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


class TestCreateRedFlagSequenceBuilder(TestCase):

    def setUp(self):
        self.__set_red_flag_request: ISetRedFlagRequestCommand = Mock()
        self.__validate_red_flag_request: IValidateRedFlagRequestCommand = Mock()
        self.__create_red_flag_command: ICreateRedFlagCommand = Mock()
        self.__set_red_flag_response: ISetCreatedAnonymousRedFlagCommand = Mock()
        self.__sut = CreateRedFlagSequenceBuilder(set_red_flag_request=self.__set_red_flag_request,
                                                  validate_red_flag_request=self.__validate_red_flag_request,
                                                  create_red_flag_command=self.__create_red_flag_command,
                                                  set_red_flag_response=self.__set_red_flag_response)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__set_red_flag_request,
            self.__validate_red_flag_request,
            self.__create_red_flag_command,
            self.__set_red_flag_response
        ])


class TestGetRedFlagsSequenceBuilder(TestCase):

    def setUp(self):
        self.__validate_get_red_flags_request: IValidatePropertyUrlCommand = Mock()
        self.__get_red_flags: IGetRedFlagsCommand = Mock()
        self.__set_red_flags_response: ISetAnonymousRedFlagsCommand = Mock()
        self.__sut = GetRedFlagsSequenceBuilder(validate_get_red_flags_request=self.__validate_get_red_flags_request,
                                                get_red_flags=self.__get_red_flags,
                                                set_red_flags_response=self.__set_red_flags_response)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__validate_get_red_flags_request,
            self.__get_red_flags,
            self.__set_red_flags_response
        ])


class TestCreateVoteForRedFlagSequenceBuilder(TestCase):

    def setUp(self):
        self.__validate_get_red_flags_request: IValidatePropertyUrlCommand = Mock()
        self.__get_red_flag_by_id: IGetRedFlagByIdCommand = Mock()
        self.__set_anonymous_red_flag_response: ISetAnonymousRedFlagCommand = Mock()
        self.__sut = CreateVoteForRedFlagSequenceBuilder(
            validate_get_red_flags_request=self.__validate_get_red_flags_request,
            get_red_flag_by_id=self.__get_red_flag_by_id,
            set_anonymous_red_flag_response=self.__set_anonymous_red_flag_response)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__validate_get_red_flags_request,
            self.__get_red_flag_by_id,
            self.__set_anonymous_red_flag_response
        ])


class TestDeleteVoteForRedFlagSequenceBuilder(TestCase):

    def setUp(self):
        self.__validate_get_red_flags_request: IValidatePropertyUrlCommand = Mock()
        self.__get_red_flag_by_id: IGetRedFlagByIdCommand = Mock()
        self.__set_anonymous_red_flag_response: ISetAnonymousRedFlagCommand = Mock()
        self.__validate_user_already_voted: IValidateAlreadyVotedCommand = Mock()
        self.__sut = DeleteVoteForRedFlagSequenceBuilder(
            validate_get_red_flags_request=self.__validate_get_red_flags_request,
            get_red_flag_by_id=self.__get_red_flag_by_id,
            set_anonymous_red_flag_response=self.__set_anonymous_red_flag_response,
            validate_user_already_voted=self.__validate_user_already_voted)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [
            self.__validate_get_red_flags_request,
            self.__get_red_flag_by_id,
            self.__validate_user_already_voted,
            self.__set_anonymous_red_flag_response
        ])

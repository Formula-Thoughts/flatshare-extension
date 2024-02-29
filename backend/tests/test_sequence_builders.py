from unittest import TestCase
from unittest.mock import Mock

from src.core import IValidateGroupCommand, ISetGroupRequestCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IValidateIfUserBelongsToAtLeastOneGroupCommand, IValidateIfGroupBelongsToUser, \
    IFetchGroupByIdCommand
from src.domain.sequence_builders import CreateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder, \
    UpsertUserGroupsBackgroundSequenceBuilder, FetchUserGroupsSequenceBuilder, GetUserGroupByIdSequenceBuilder


class TestCreateGroupAsyncSequenceBuilder(TestCase):

    def setUp(self):
        self.__save: ICreateGroupAsyncCommand = Mock()
        self.__build_request: ISetGroupRequestCommand = Mock()
        self.__validate_request: IValidateGroupCommand = Mock()
        self.__create_user_group: ICreateUserGroupsAsyncCommand = Mock()
        self.__validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand = Mock()
        self.__sut = CreateGroupSequenceBuilder(set_group_request=self.__build_request,
                                                validate_group=self.__validate_request,
                                                save_group_async=self.__save,
                                                create_user_group_async=self.__create_user_group,
                                                validate_if_user_belongs_to_at_least_one_group_command=self.__validate_if_user_belongs_to_at_least_one_group_command)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__build_request,
                                                 self.__validate_request,
                                                 self.__validate_if_user_belongs_to_at_least_one_group_command,
                                                 self.__save,
                                                 self.__create_user_group])


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

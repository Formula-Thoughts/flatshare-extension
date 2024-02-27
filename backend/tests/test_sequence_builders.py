from unittest import TestCase
from unittest.mock import Mock

from src.core import IValidateGroupCommand, ISetGroupRequestCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand
from src.domain.sequence_builders import CreateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder


class TestCreateGroupAsyncSequenceBuilder(TestCase):

    def setUp(self):
        self.__save: ICreateGroupAsyncCommand = Mock()
        self.__build_request: ISetGroupRequestCommand = Mock()
        self.__validate_request: IValidateGroupCommand = Mock()
        self.__sut = CreateGroupSequenceBuilder(set_group_request=self.__build_request,
                                                validate_group=self.__validate_request,
                                                save_group_async=self.__save)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__build_request,
                                                 self.__validate_request,
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
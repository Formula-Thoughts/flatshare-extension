from unittest import TestCase
from unittest.mock import Mock

from backend.src.core import ValidateGroupCommand, SetGroupRequestCommand, CreateGroupAsyncCommand
from backend.src.domain.sequence_builders import CreateGroupAsyncSequenceBuilder


class TestCreateGroupAsyncSequenceBuilder(TestCase):

    def setUp(self):
        self.__save: CreateGroupAsyncCommand = Mock()
        self.__build_request: SetGroupRequestCommand = Mock()
        self.__validate_request: ValidateGroupCommand = Mock()
        self.__sut = CreateGroupAsyncSequenceBuilder(set_group_request=self.__build_request,
                                                     validate_group=self.__validate_request,
                                                     save_group_async=self.__save)

    def test_build_should_run_commands_in_order(self):
        # act
        self.__sut.build()

        # assert
        self.assertEqual(self.__sut.components, [self.__build_request,
                                                 self.__validate_request,
                                                 self.__save])
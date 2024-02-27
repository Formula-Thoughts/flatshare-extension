from formula_thoughts_web.application import FluentSequenceBuilder

from backend.src.core import SetGroupRequestCommand, ValidateGroupCommand, CreateGroupAsyncCommand


class CreateGroupAsyncSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, set_group_request: SetGroupRequestCommand,
                 validate_group: ValidateGroupCommand,
                 save_group_async: CreateGroupAsyncCommand):
        self.__save_group_async = save_group_async
        self.__validate_group = validate_group
        self.__set_group_request = set_group_request
        super().__init__()

    def build(self):
        self._add_command(command=self.__set_group_request)\
            ._add_command(command=self.__validate_group)\
            ._add_command(command=self.__save_group_async)

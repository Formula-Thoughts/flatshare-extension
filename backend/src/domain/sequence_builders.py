from formula_thoughts_web.application import FluentSequenceBuilder

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundCommand


class CreateGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, set_group_request: ISetGroupRequestCommand,
                 validate_group: IValidateGroupCommand,
                 save_group_async: ICreateGroupAsyncCommand,
                 create_user_group_async: ICreateUserGroupsAsyncCommand):
        self.__create_user_group_async = create_user_group_async
        self.__save_group_async = save_group_async
        self.__validate_group = validate_group
        self.__set_group_request = set_group_request
        super().__init__()

    def build(self):
        self._add_command(command=self.__set_group_request)\
            ._add_command(command=self.__validate_group)\
            ._add_command(command=self.__save_group_async) \
            ._add_command(command=self.__create_user_group_async)


class UpsertGroupBackgroundSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, upsert_background_command: IUpsertGroupBackgroundCommand):
        self.__upsert_background_command = upsert_background_command
        super().__init__()

    def build(self):
        self._add_command(command=self.__upsert_background_command)


class UpsertUserGroupsBackgroundSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, upsert_background_command: IUpsertUserGroupsBackgroundCommand):
        self.__upsert_background_command = upsert_background_command
        super().__init__()

    def build(self):
        ...
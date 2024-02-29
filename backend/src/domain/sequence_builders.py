from formula_thoughts_web.application import FluentSequenceBuilder

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IValidateIfUserBelongsToAtLeastOneGroupCommand, IValidateIfGroupBelongsToUser, \
    IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetFlatRequestCommand, ICreateFlatCommand


class CreateGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, set_group_request: ISetGroupRequestCommand,
                 validate_group: IValidateGroupCommand,
                 validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 save_group_async: ICreateGroupAsyncCommand,
                 create_user_group_async: ICreateUserGroupsAsyncCommand):
        self.__validate_if_user_belongs_to_at_least_one_group_command = validate_if_user_belongs_to_at_least_one_group_command
        self.__create_user_group_async = create_user_group_async
        self.__save_group_async = save_group_async
        self.__validate_group = validate_group
        self.__set_group_request = set_group_request
        super().__init__()

    def build(self):
        self._add_command(command=self.__set_group_request)\
            ._add_command(command=self.__validate_group)\
            ._add_command(command=self.__validate_if_user_belongs_to_at_least_one_group_command)\
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
        self._add_command(command=self.__upsert_background_command)


class FetchUserGroupsSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, fetch_user_group_command: IFetchUserGroupsCommand):
        super().__init__()
        self.__fetch_user_group_command = fetch_user_group_command

    def build(self):
        self._add_command(command=self.__fetch_user_group_command)


class GetUserGroupByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUser,
                 fetch_group_by_id_command: IFetchGroupByIdCommand):
        super().__init__()
        self.__fetch_group_by_id_command = fetch_group_by_id_command
        self.__validate_if_group_belongs_to_user = validate_if_group_belongs_to_user
        self.__validate_if_user_belongs_to_at_least_one_group_command = validate_if_user_belongs_to_at_least_one_group_command

    def build(self):
        self._add_command(command=self.__validate_if_user_belongs_to_at_least_one_group_command)\
            ._add_command(command=self.__validate_if_group_belongs_to_user)\
            ._add_command(command=self.__fetch_group_by_id_command)


class CreateFlatSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 get_user_group_by_id: IGetUserGroupByIdSequenceBuilder,
                 set_create_flat_request: ISetFlatRequestCommand,
                 create_flat: ICreateFlatCommand):
        self.__create_flat = create_flat
        self.__set_create_flat_request_command = set_create_flat_request
        self.__get_user_group_by_id_command = get_user_group_by_id
        super().__init__()

    def build(self):
        pass

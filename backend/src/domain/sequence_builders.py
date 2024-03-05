from formula_thoughts_web.application import FluentSequenceBuilder

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, IUpdateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IValidateIfUserBelongsToAtLeastOneGroupCommand, IValidateIfGroupBelongsToUser, \
    IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetFlatRequestCommand, ICreateFlatCommand, \
    IValidateFlatRequestCommand, IDeleteFlatCommand, IAddUserToGroupSequenceBuilder, IAddCurrentUserToGroupCommand, \
    ISetGroupIdFromCodeCommand, IGetCodeFromGroupIdCommand, IValidateUserIsNotParticipantCommand, \
    ICreateGroupAsyncCommand


class UpdateGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, set_group_request: ISetGroupRequestCommand,
                 validate_group: IValidateGroupCommand,
                 validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUser,
                 fetch_group_by_id: IFetchGroupByIdCommand,
                 save_group_async: IUpdateGroupAsyncCommand):
        self.__fetch_group_by_id = fetch_group_by_id
        self.__validate_if_group_belongs_to_user = validate_if_group_belongs_to_user
        self.__validate_if_user_belongs_to_at_least_one_group_command = validate_if_user_belongs_to_at_least_one_group_command
        self.__save_group_async = save_group_async
        self.__validate_group = validate_group
        self.__set_group_request = set_group_request
        super().__init__()

    def build(self):
        self._add_command(command=self.__set_group_request)\
            ._add_command(command=self.__validate_group)\
            ._add_command(command=self.__validate_if_user_belongs_to_at_least_one_group_command)\
            ._add_command(command=self.__validate_if_group_belongs_to_user)\
            ._add_command(command=self.__fetch_group_by_id)\
            ._add_command(command=self.__save_group_async)


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
                 create_flat: ICreateFlatCommand,
                 validate_flat: IValidateFlatRequestCommand):
        self.__validate_flat = validate_flat
        self.__create_flat = create_flat
        self.__set_create_flat_request = set_create_flat_request
        self.__get_user_group_by_id = get_user_group_by_id
        super().__init__()

    def build(self):
        self._add_command(self.__set_create_flat_request)\
            ._add_sequence_builder(self.__get_user_group_by_id)\
            ._add_command(self.__validate_flat)\
            ._add_command(self.__create_flat)


class DeleteFlatSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 get_user_group_by_id: IGetUserGroupByIdSequenceBuilder,
                 delete_flat: IDeleteFlatCommand):
        self.__delete_flat = delete_flat
        self.__get_user_group_by_id = get_user_group_by_id
        super().__init__()

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__get_user_group_by_id)\
            ._add_command(command=self.__delete_flat)


class AddUserToGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 set_group_id_from_code: ISetGroupIdFromCodeCommand,
                 get_group_by_id: IFetchGroupByIdCommand,
                 validate_user_is_not_participant: IValidateUserIsNotParticipantCommand,
                 add_current_user_to_group_command: IAddCurrentUserToGroupCommand,
                 create_user_groups: ICreateUserGroupsAsyncCommand):
        self.__create_user_groups = create_user_groups
        self.__validate_user_is_not_participant = validate_user_is_not_participant
        self.__set_group_id_from_code = set_group_id_from_code
        self.__add_current_user_to_group_command = add_current_user_to_group_command
        self.__get_group_by_id = get_group_by_id
        super().__init__()

    def build(self):
        self._add_command(command=self.__set_group_id_from_code)\
            ._add_command(command=self.__get_group_by_id)\
            ._add_command(command=self.__validate_user_is_not_participant)\
            ._add_command(command=self.__add_current_user_to_group_command)\
            ._add_command(command=self.__create_user_groups)


class GetCodeForGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, get_group_by_id_sequence: IGetUserGroupByIdSequenceBuilder,
                 get_code_from_group_id: IGetCodeFromGroupIdCommand):
        super().__init__()
        self.__get_group_by_id_sequence = get_group_by_id_sequence
        self.__get_code_from_group_id = get_code_from_group_id

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__get_group_by_id_sequence)\
            ._add_command(command=self.__get_code_from_group_id)


class CreateGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, validate_user_belongs_to_one_group: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 create_user_groups: ICreateUserGroupsAsyncCommand,
                 create_group: ICreateGroupAsyncCommand):
        super().__init__()
        self.__create_group = create_group
        self.__create_user_groups = create_user_groups
        self.__validate_user_belongs_to_one_group = validate_user_belongs_to_one_group

    def build(self):
        self._add_command(command=self.__validate_user_belongs_to_one_group)\
            ._add_command(command=self.__create_group)\
            ._add_command(command=self.__create_user_groups)
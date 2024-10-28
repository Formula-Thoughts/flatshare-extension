from formula_thoughts_web.application import FluentSequenceBuilder

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, \
    IFetchUserGroupsCommand, IValidateIfUserBelongsToAtLeastOneGroupCommand, IValidateIfGroupBelongsToUserCommand, \
    IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetPropertyRequestCommand, ICreatePropertyCommand, \
    IValidatePropertyRequestCommand, IDeletePropertyCommand, IAddCurrentUserToGroupCommand, \
    ISetGroupIdFromCodeCommand, IGetCodeFromGroupIdCommand, IValidateUserIsNotParticipantCommand, \
    IFetchAuthUserClaimsIfUserDoesNotExistCommand, IFetchUserGroupIfExistsSequenceBuilder, \
    ICreateGroupCommand, ICreateUserGroupsCommand, IUpdateGroupCommand, ISetRedFlagRequestCommand, \
    IValidateRedFlagRequestCommand, ICreateRedFlagCommand, ISetCreatedAnonymousRedFlagCommand, \
    IValidatePropertyUrlCommand, IGetRedFlagsCommand, ISetAnonymousRedFlagsCommand, IGetRedFlagByIdCommand, \
    ISetAnonymousRedFlagCommand, IValidateAlreadyVotedCommand, IValidateNotVotedCommand, ICreateVoteCommand, \
    IDeleteVoteCommand, IValidateUserIsAlreadyParticipantCommand, IRemoveGroupFromUserGroupsCommand, \
    IRemoveParticipantFromGroupCommand


class UpdateGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, set_group_request: ISetGroupRequestCommand,
                 validate_group: IValidateGroupCommand,
                 validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUserCommand,
                 fetch_group_by_id: IFetchGroupByIdCommand,
                 update_group: IUpdateGroupCommand):
        self.__fetch_group_by_id = fetch_group_by_id
        self.__validate_if_group_belongs_to_user = validate_if_group_belongs_to_user
        self.__validate_if_user_belongs_to_at_least_one_group_command = validate_if_user_belongs_to_at_least_one_group_command
        self.__update_group = update_group
        self.__validate_group = validate_group
        self.__set_group_request = set_group_request
        super().__init__()

    def build(self):
        self._add_command(command=self.__set_group_request) \
            ._add_command(command=self.__validate_group) \
            ._add_command(command=self.__validate_if_user_belongs_to_at_least_one_group_command) \
            ._add_command(command=self.__validate_if_group_belongs_to_user) \
            ._add_command(command=self.__fetch_group_by_id) \
            ._add_command(command=self.__update_group)


class FetchUserGroupsSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, fetch_user_group_command: IFetchUserGroupsCommand):
        super().__init__()
        self.__fetch_user_group_command = fetch_user_group_command

    def build(self):
        self._add_command(command=self.__fetch_user_group_command)


class GetUserGroupByIdSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 validate_if_user_belongs_to_at_least_one_group_command: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 validate_if_group_belongs_to_user: IValidateIfGroupBelongsToUserCommand,
                 fetch_group_by_id_command: IFetchGroupByIdCommand):
        super().__init__()
        self.__fetch_group_by_id_command = fetch_group_by_id_command
        self.__validate_if_group_belongs_to_user = validate_if_group_belongs_to_user
        self.__validate_if_user_belongs_to_at_least_one_group_command = validate_if_user_belongs_to_at_least_one_group_command

    def build(self):
        self._add_command(command=self.__validate_if_user_belongs_to_at_least_one_group_command) \
            ._add_command(command=self.__validate_if_group_belongs_to_user) \
            ._add_command(command=self.__fetch_group_by_id_command)


class CreatePropertySequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 get_user_group_by_id: IGetUserGroupByIdSequenceBuilder,
                 set_create_property_request: ISetPropertyRequestCommand,
                 create_property: ICreatePropertyCommand,
                 validate_property: IValidatePropertyRequestCommand):
        self.__validate_property = validate_property
        self.__create_property = create_property
        self.__set_create_property_request = set_create_property_request
        self.__get_user_group_by_id = get_user_group_by_id
        super().__init__()

    def build(self):
        self._add_command(self.__set_create_property_request) \
            ._add_sequence_builder(self.__get_user_group_by_id) \
            ._add_command(self.__validate_property) \
            ._add_command(self.__create_property)


class DeletePropertySequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 get_user_group_by_id: IGetUserGroupByIdSequenceBuilder,
                 delete_property: IDeletePropertyCommand):
        self.__delete_property = delete_property
        self.__get_user_group_by_id = get_user_group_by_id
        super().__init__()

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__get_user_group_by_id) \
            ._add_command(command=self.__delete_property)


class AddUserToGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self,
                 fetch_user_group_if_exists: IFetchUserGroupIfExistsSequenceBuilder,
                 set_group_id_from_code: ISetGroupIdFromCodeCommand,
                 get_group_by_id: IFetchGroupByIdCommand,
                 validate_user_is_not_participant: IValidateUserIsNotParticipantCommand,
                 add_current_user_to_group_command: IAddCurrentUserToGroupCommand,
                 create_user_groups: ICreateUserGroupsCommand):
        self.__fetch_user_group_if_exists = fetch_user_group_if_exists
        self.__create_user_groups = create_user_groups
        self.__validate_user_is_not_participant = validate_user_is_not_participant
        self.__set_group_id_from_code = set_group_id_from_code
        self.__add_current_user_to_group_command = add_current_user_to_group_command
        self.__get_group_by_id = get_group_by_id
        super().__init__()

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__fetch_user_group_if_exists) \
            ._add_command(command=self.__set_group_id_from_code) \
            ._add_command(command=self.__get_group_by_id) \
            ._add_command(command=self.__validate_user_is_not_participant) \
            ._add_command(command=self.__add_current_user_to_group_command) \
            ._add_command(command=self.__create_user_groups)


class GetCodeForGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, get_group_by_id_sequence: IGetUserGroupByIdSequenceBuilder,
                 get_code_from_group_id: IGetCodeFromGroupIdCommand):
        super().__init__()
        self.__get_group_by_id_sequence = get_group_by_id_sequence
        self.__get_code_from_group_id = get_code_from_group_id

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__get_group_by_id_sequence) \
            ._add_command(command=self.__get_code_from_group_id)


class CreateGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, fetch_user_group_if_exists: IFetchUserGroupIfExistsSequenceBuilder,
                 create_user_groups: ICreateUserGroupsCommand,
                 create_group: ICreateGroupCommand):
        super().__init__()
        self.__fetch_user_group_if_exists = fetch_user_group_if_exists
        self.__create_group = create_group
        self.__create_user_groups = create_user_groups

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__fetch_user_group_if_exists) \
            ._add_command(command=self.__create_group) \
            ._add_command(command=self.__create_user_groups)


class FetchUserGroupIfExistsSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, validate_user_belongs_to_at_least_one_group: IValidateIfUserBelongsToAtLeastOneGroupCommand,
                 fetch_auth_claims_if_user_has_no_group: IFetchAuthUserClaimsIfUserDoesNotExistCommand):
        super().__init__()
        self.__fetch_auth_claims_if_user_has_no_group = fetch_auth_claims_if_user_has_no_group
        self.__validate_user_belongs_to_at_least_one_group = validate_user_belongs_to_at_least_one_group

    def build(self):
        self._add_command(command=self.__validate_user_belongs_to_at_least_one_group) \
            ._add_command(command=self.__fetch_auth_claims_if_user_has_no_group)


class CreateRedFlagSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, set_red_flag_request: ISetRedFlagRequestCommand,
                 validate_red_flag_request: IValidateRedFlagRequestCommand,
                 create_red_flag_command: ICreateRedFlagCommand,
                 set_red_flag_response: ISetCreatedAnonymousRedFlagCommand):
        super().__init__()
        self.__set_red_flag_response = set_red_flag_response
        self.__create_red_flag_command = create_red_flag_command
        self.__validate_red_flag_request = validate_red_flag_request
        self.__set_red_flag_request = set_red_flag_request

    def build(self):
        self._add_command(command=self.__set_red_flag_request) \
            ._add_command(command=self.__validate_red_flag_request) \
            ._add_command(command=self.__create_red_flag_command) \
            ._add_command(command=self.__set_red_flag_response)


class GetRedFlagsSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, validate_get_red_flags_request: IValidatePropertyUrlCommand,
                 get_red_flags: IGetRedFlagsCommand,
                 set_red_flags_response: ISetAnonymousRedFlagsCommand):
        super().__init__()
        self.__set_red_flags_response = set_red_flags_response
        self.__get_red_flags = get_red_flags
        self.__validate_get_red_flags_request = validate_get_red_flags_request

    def build(self):
        self._add_command(command=self.__validate_get_red_flags_request) \
            ._add_command(command=self.__get_red_flags) \
            ._add_command(command=self.__set_red_flags_response)


class CreateVoteForRedFlagSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, validate_get_red_flags_request: IValidatePropertyUrlCommand,
                 get_red_flag_by_id: IGetRedFlagByIdCommand,
                 validate_not_voted: IValidateNotVotedCommand,
                 upvote: ICreateVoteCommand,
                 set_anonymous_red_flag_response: ISetAnonymousRedFlagCommand):
        super().__init__()
        self.__upvote = upvote
        self.__validate_not_voted = validate_not_voted
        self.__set_anonymous_red_flag_response = set_anonymous_red_flag_response
        self.__get_red_flag_by_id = get_red_flag_by_id
        self.__validate_get_red_flags_request = validate_get_red_flags_request

    def build(self):
        self._add_command(command=self.__validate_get_red_flags_request) \
            ._add_command(command=self.__get_red_flag_by_id) \
            ._add_command(command=self.__validate_not_voted) \
            ._add_command(command=self.__upvote) \
            ._add_command(command=self.__set_anonymous_red_flag_response)


class DeleteVoteForRedFlagSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, validate_get_red_flags_request: IValidatePropertyUrlCommand,
                 get_red_flag_by_id: IGetRedFlagByIdCommand,
                 validate_user_already_voted: IValidateAlreadyVotedCommand,
                 down_vote_command: IDeleteVoteCommand,
                 set_anonymous_red_flag_response: ISetAnonymousRedFlagCommand):
        super().__init__()
        self.__down_vote_command = down_vote_command
        self.__validate_user_already_voted = validate_user_already_voted
        self.__set_anonymous_red_flag_response = set_anonymous_red_flag_response
        self.__get_red_flag_by_id = get_red_flag_by_id
        self.__validate_get_red_flags_request = validate_get_red_flags_request

    def build(self):
        self._add_command(command=self.__validate_get_red_flags_request) \
            ._add_command(command=self.__get_red_flag_by_id) \
            ._add_command(command=self.__validate_user_already_voted) \
            ._add_command(command=self.__down_vote_command) \
            ._add_command(command=self.__set_anonymous_red_flag_response)


class RemoveUserFromGroupSequenceBuilder(FluentSequenceBuilder):

    def __init__(self, fetch_user_group_if_exists: IFetchUserGroupIfExistsSequenceBuilder,
                 get_group_by_id: IFetchGroupByIdCommand,
                 validate_user_is_already_participant: IValidateUserIsAlreadyParticipantCommand,
                 remove_group_from_user_groups_command: IRemoveGroupFromUserGroupsCommand,
                 remove_participant_from_group_command: IRemoveParticipantFromGroupCommand):
        super().__init__()
        self.__remove_participant_from_group_command = remove_participant_from_group_command
        self.__remove_group_from_user_groups_command = remove_group_from_user_groups_command
        self.__validate_user_is_already_participant = validate_user_is_already_participant
        self.__get_group_by_id = get_group_by_id
        self.__fetch_user_group_if_exists = fetch_user_group_if_exists

    def build(self):
        self._add_sequence_builder(sequence_builder=self.__fetch_user_group_if_exists) \
            ._add_command(command=self.__get_group_by_id) \
            ._add_command(command=self.__validate_user_is_already_participant) \
            ._add_command(command=self.__remove_participant_from_group_command) \
            ._add_command(command=self.__remove_group_from_user_groups_command)

from formula_thoughts_web.ioc import Container

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, IUpdateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, IUpdateGroupSequenceBuilder, IUpsertGroupBackgroundSequenceBuilder, \
    ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundSequenceBuilder, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IFetchUserGroupsSequenceBuilder, IValidateIfUserBelongsToAtLeastOneGroupCommand, \
    IValidateIfGroupBelongsToUser, IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetFlatRequestCommand, \
    ICreateFlatCommand, ICreateFlatSequenceBuilder, IValidateFlatRequestCommand, IDeleteFlatCommand, \
    IDeleteFlatSequenceBuilder, IAddCurrentUserToGroupCommand, IAddUserToGroupSequenceBuilder, \
    ISetGroupIdFromCodeCommand, IGetCodeFromGroupIdCommand, IGetCodeForGroupSequenceBuilder, \
    IValidateUserIsNotParticipantCommand, ICreateGroupAsyncCommand, ICreateGroupSequenceBuilder, \
    IFetchAuthUserClaimsCommand
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, UpdateGroupAsyncCommand, \
    UpsertGroupBackgroundCommand, CreateUserGroupsAsyncCommand, UpsertUserGroupsBackgroundCommand, \
    FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, ValidateIfGroupBelongsToUser, \
    FetchGroupByIdCommand, SetFlatRequestCommand, CreateFlatCommand, ValidateFlatRequestCommand, DeleteFlatCommand, \
    AddCurrentUserToGroupCommand, SetGroupIdFromCodeCommand, GetCodeFromGroupIdCommand, \
    ValidateUserIsNotParticipantCommand, CreateGroupAsyncCommand, FetchAuthUserClaimsCommand
from src.domain.sequence_builders import UpdateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder, \
    UpsertUserGroupsBackgroundSequenceBuilder, FetchUserGroupsSequenceBuilder, GetUserGroupByIdSequenceBuilder, \
    CreateFlatSequenceBuilder, DeleteFlatSequenceBuilder, AddUserToGroupSequenceBuilder, GetCodeForGroupSequenceBuilder, \
    CreateGroupSequenceBuilder


def register_domain_dependencies(container: Container):
    (container.register(service=ISetGroupRequestCommand, implementation=SetGroupRequestCommand)
     .register(service=IValidateGroupCommand, implementation=ValidateGroupCommand)
     .register(service=IUpdateGroupAsyncCommand, implementation=UpdateGroupAsyncCommand)
     .register(service=ICreateGroupAsyncCommand, implementation=CreateGroupAsyncCommand)
     .register(service=ICreateUserGroupsAsyncCommand, implementation=CreateUserGroupsAsyncCommand)
     .register(service=IUpsertGroupBackgroundCommand, implementation=UpsertGroupBackgroundCommand)
     .register(service=IFetchUserGroupsCommand, implementation=FetchUserGroupsCommand)
     .register(service=IUpsertUserGroupsBackgroundCommand, implementation=UpsertUserGroupsBackgroundCommand)
     .register(service=IUpdateGroupSequenceBuilder, implementation=UpdateGroupSequenceBuilder)
     .register(service=IUpsertGroupBackgroundSequenceBuilder, implementation=UpsertGroupBackgroundSequenceBuilder)
     .register(service=IFetchUserGroupsSequenceBuilder, implementation=FetchUserGroupsSequenceBuilder)
     .register(service=IFetchGroupByIdCommand, implementation=FetchGroupByIdCommand)
     .register(service=ISetFlatRequestCommand, implementation=SetFlatRequestCommand)
     .register(service=ICreateFlatCommand, implementation=CreateFlatCommand)
     .register(service=IDeleteFlatCommand, implementation=DeleteFlatCommand)
     .register(service=ISetGroupIdFromCodeCommand, implementation=SetGroupIdFromCodeCommand)
     .register(service=IGetCodeFromGroupIdCommand, implementation=GetCodeFromGroupIdCommand)
     .register(service=IAddCurrentUserToGroupCommand, implementation=AddCurrentUserToGroupCommand)
     .register(service=IValidateFlatRequestCommand, implementation=ValidateFlatRequestCommand)
     .register(service=IFetchAuthUserClaimsCommand, implementation=FetchAuthUserClaimsCommand)
     .register(service=IValidateUserIsNotParticipantCommand, implementation=ValidateUserIsNotParticipantCommand)
     .register(service=IValidateIfGroupBelongsToUser,
               implementation=ValidateIfGroupBelongsToUser)
     .register(service=IValidateIfUserBelongsToAtLeastOneGroupCommand,
               implementation=ValidateIfUserBelongsToAtLeastOneGroupCommand)
     .register(service=IUpsertUserGroupsBackgroundSequenceBuilder,
               implementation=UpsertUserGroupsBackgroundSequenceBuilder)
     .register(service=IGetUserGroupByIdSequenceBuilder,
               implementation=GetUserGroupByIdSequenceBuilder)
     .register(service=ICreateFlatSequenceBuilder,
               implementation=CreateFlatSequenceBuilder)
     .register(service=IDeleteFlatSequenceBuilder,
               implementation=DeleteFlatSequenceBuilder)
     .register(service=IAddUserToGroupSequenceBuilder,
               implementation=AddUserToGroupSequenceBuilder)
     .register(service=IGetCodeForGroupSequenceBuilder,
               implementation=GetCodeForGroupSequenceBuilder)
     .register(service=ICreateGroupSequenceBuilder,
               implementation=CreateGroupSequenceBuilder))

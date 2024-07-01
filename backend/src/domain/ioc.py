from formula_thoughts_web.ioc import Container

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, IUpdateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, IUpdateGroupSequenceBuilder, IUpsertGroupBackgroundSequenceBuilder, \
    ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundSequenceBuilder, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IFetchUserGroupsSequenceBuilder, IValidateIfUserBelongsToAtLeastOneGroupCommand, \
    IValidateIfGroupBelongsToUserCommand, IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetPropertyRequestCommand, \
    ICreatePropertyCommand, ICreatePropertySequenceBuilder, IValidatePropertyRequestCommand, IDeletePropertyCommand, \
    IDeletePropertySequenceBuilder, IAddCurrentUserToGroupCommand, IAddUserToGroupSequenceBuilder, \
    ISetGroupIdFromCodeCommand, IGetCodeFromGroupIdCommand, IGetCodeForGroupSequenceBuilder, \
    IValidateUserIsNotParticipantCommand, ICreateGroupAsyncCommand, ICreateGroupSequenceBuilder, \
    IFetchAuthUserClaimsIfUserDoesNotExistCommand, IFetchUserGroupIfExistsSequenceBuilder, ICreateUserGroupsCommand, \
    ICreateGroupCommand
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, UpdateGroupAsyncCommand, \
    UpsertGroupBackgroundCommand, CreateUserGroupsAsyncCommand, UpsertUserGroupsBackgroundCommand, \
    FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, ValidateIfGroupBelongsToUserCommand, \
    FetchGroupByIdCommand, SetPropertyRequestCommand, CreatePropertyCommand, ValidatePropertyRequestCommand, \
    DeletePropertyCommand, \
    AddCurrentUserToGroupCommand, SetGroupIdFromCodeCommand, GetCodeFromGroupIdCommand, \
    ValidateUserIsNotParticipantCommand, CreateGroupAsyncCommand, FetchAuthUserClaimsIfUserDoesNotExistCommand, \
    CreateUserGroupsCommand, CreateGroupCommand
from src.domain.sequence_builders import UpdateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder, \
    UpsertUserGroupsBackgroundSequenceBuilder, FetchUserGroupsSequenceBuilder, GetUserGroupByIdSequenceBuilder, \
    CreatePropertySequenceBuilder, DeletePropertySequenceBuilder, AddUserToGroupSequenceBuilder, GetCodeForGroupSequenceBuilder, \
    CreateGroupSequenceBuilder, FetchUserGroupIfExistsSequenceBuilder


def register_domain_dependencies(container: Container):
    (container.register(service=ISetGroupRequestCommand, implementation=SetGroupRequestCommand)
     .register(service=IValidateGroupCommand, implementation=ValidateGroupCommand)
     .register(service=IUpdateGroupAsyncCommand, implementation=UpdateGroupAsyncCommand)
     .register(service=ICreateGroupAsyncCommand, implementation=CreateGroupAsyncCommand)
     .register(service=ICreateUserGroupsCommand, implementation=CreateUserGroupsCommand)
     .register(service=ICreateGroupCommand, implementation=CreateGroupCommand)
     .register(service=ICreateUserGroupsAsyncCommand, implementation=CreateUserGroupsAsyncCommand)
     .register(service=IUpsertGroupBackgroundCommand, implementation=UpsertGroupBackgroundCommand)
     .register(service=IFetchUserGroupsCommand, implementation=FetchUserGroupsCommand)
     .register(service=IUpsertUserGroupsBackgroundCommand, implementation=UpsertUserGroupsBackgroundCommand)
     .register(service=IUpdateGroupSequenceBuilder, implementation=UpdateGroupSequenceBuilder)
     .register(service=IUpsertGroupBackgroundSequenceBuilder, implementation=UpsertGroupBackgroundSequenceBuilder)
     .register(service=IFetchUserGroupsSequenceBuilder, implementation=FetchUserGroupsSequenceBuilder)
     .register(service=IFetchGroupByIdCommand, implementation=FetchGroupByIdCommand)
     .register(service=ISetPropertyRequestCommand, implementation=SetPropertyRequestCommand)
     .register(service=ICreatePropertyCommand, implementation=CreatePropertyCommand)
     .register(service=IDeletePropertyCommand, implementation=DeletePropertyCommand)
     .register(service=ISetGroupIdFromCodeCommand, implementation=SetGroupIdFromCodeCommand)
     .register(service=IGetCodeFromGroupIdCommand, implementation=GetCodeFromGroupIdCommand)
     .register(service=IAddCurrentUserToGroupCommand, implementation=AddCurrentUserToGroupCommand)
     .register(service=IValidatePropertyRequestCommand, implementation=ValidatePropertyRequestCommand)
     .register(service=IFetchAuthUserClaimsIfUserDoesNotExistCommand, implementation=FetchAuthUserClaimsIfUserDoesNotExistCommand)
     .register(service=IValidateUserIsNotParticipantCommand, implementation=ValidateUserIsNotParticipantCommand)
     .register(service=IValidateIfGroupBelongsToUserCommand,
               implementation=ValidateIfGroupBelongsToUserCommand)
     .register(service=IValidateIfUserBelongsToAtLeastOneGroupCommand,
               implementation=ValidateIfUserBelongsToAtLeastOneGroupCommand)
     .register(service=IUpsertUserGroupsBackgroundSequenceBuilder,
               implementation=UpsertUserGroupsBackgroundSequenceBuilder)
     .register(service=IGetUserGroupByIdSequenceBuilder,
               implementation=GetUserGroupByIdSequenceBuilder)
     .register(service=ICreatePropertySequenceBuilder,
               implementation=CreatePropertySequenceBuilder)
     .register(service=IDeletePropertySequenceBuilder,
               implementation=DeletePropertySequenceBuilder)
     .register(service=IAddUserToGroupSequenceBuilder,
               implementation=AddUserToGroupSequenceBuilder)
     .register(service=IGetCodeForGroupSequenceBuilder,
               implementation=GetCodeForGroupSequenceBuilder)
     .register(service=ICreateGroupSequenceBuilder,
               implementation=CreateGroupSequenceBuilder)
     .register(service=IFetchUserGroupIfExistsSequenceBuilder,
               implementation=FetchUserGroupIfExistsSequenceBuilder))

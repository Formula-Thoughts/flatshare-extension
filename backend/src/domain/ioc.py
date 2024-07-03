from formula_thoughts_web.ioc import Container

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, IUpdateGroupSequenceBuilder, \
    IFetchUserGroupsCommand, IFetchUserGroupsSequenceBuilder, IValidateIfUserBelongsToAtLeastOneGroupCommand, \
    IValidateIfGroupBelongsToUserCommand, IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, \
    ISetPropertyRequestCommand, \
    ICreatePropertyCommand, ICreatePropertySequenceBuilder, IValidatePropertyRequestCommand, IDeletePropertyCommand, \
    IDeletePropertySequenceBuilder, IAddCurrentUserToGroupCommand, IAddUserToGroupSequenceBuilder, \
    ISetGroupIdFromCodeCommand, IGetCodeFromGroupIdCommand, IGetCodeForGroupSequenceBuilder, \
    IValidateUserIsNotParticipantCommand, ICreateGroupSequenceBuilder, \
    IFetchAuthUserClaimsIfUserDoesNotExistCommand, IFetchUserGroupIfExistsSequenceBuilder, ICreateUserGroupsCommand, \
    ICreateGroupCommand, IUpdateGroupCommand
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, \
    FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, ValidateIfGroupBelongsToUserCommand, \
    FetchGroupByIdCommand, SetPropertyRequestCommand, CreatePropertyCommand, ValidatePropertyRequestCommand, \
    DeletePropertyCommand, \
    AddCurrentUserToGroupCommand, SetGroupIdFromCodeCommand, GetCodeFromGroupIdCommand, \
    ValidateUserIsNotParticipantCommand, FetchAuthUserClaimsIfUserDoesNotExistCommand, \
    CreateUserGroupsCommand, CreateGroupCommand, UpdateGroupCommand
from src.domain.sequence_builders import UpdateGroupSequenceBuilder, FetchUserGroupsSequenceBuilder, \
    GetUserGroupByIdSequenceBuilder, \
    CreatePropertySequenceBuilder, DeletePropertySequenceBuilder, AddUserToGroupSequenceBuilder, \
    GetCodeForGroupSequenceBuilder, \
    CreateGroupSequenceBuilder, FetchUserGroupIfExistsSequenceBuilder


def register_domain_dependencies(container: Container):
    (container.register(service=ISetGroupRequestCommand, implementation=SetGroupRequestCommand)
     .register(service=IValidateGroupCommand, implementation=ValidateGroupCommand)
     .register(service=ICreateUserGroupsCommand, implementation=CreateUserGroupsCommand)
     .register(service=ICreateGroupCommand, implementation=CreateGroupCommand)
     .register(service=IUpdateGroupCommand, implementation=UpdateGroupCommand)
     .register(service=IFetchUserGroupsCommand, implementation=FetchUserGroupsCommand)
     .register(service=IUpdateGroupSequenceBuilder, implementation=UpdateGroupSequenceBuilder)
     .register(service=IFetchUserGroupsSequenceBuilder, implementation=FetchUserGroupsSequenceBuilder)
     .register(service=IFetchGroupByIdCommand, implementation=FetchGroupByIdCommand)
     .register(service=ISetPropertyRequestCommand, implementation=SetPropertyRequestCommand)
     .register(service=ICreatePropertyCommand, implementation=CreatePropertyCommand)
     .register(service=IDeletePropertyCommand, implementation=DeletePropertyCommand)
     .register(service=ISetGroupIdFromCodeCommand, implementation=SetGroupIdFromCodeCommand)
     .register(service=IGetCodeFromGroupIdCommand, implementation=GetCodeFromGroupIdCommand)
     .register(service=IAddCurrentUserToGroupCommand, implementation=AddCurrentUserToGroupCommand)
     .register(service=IValidatePropertyRequestCommand, implementation=ValidatePropertyRequestCommand)
     .register(service=IFetchAuthUserClaimsIfUserDoesNotExistCommand,
               implementation=FetchAuthUserClaimsIfUserDoesNotExistCommand)
     .register(service=IValidateUserIsNotParticipantCommand, implementation=ValidateUserIsNotParticipantCommand)
     .register(service=IValidateIfGroupBelongsToUserCommand,
               implementation=ValidateIfGroupBelongsToUserCommand)
     .register(service=IValidateIfUserBelongsToAtLeastOneGroupCommand,
               implementation=ValidateIfUserBelongsToAtLeastOneGroupCommand)
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

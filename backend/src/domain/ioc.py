from formula_thoughts_web.ioc import Container

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateGroupSequenceBuilder, IUpsertGroupBackgroundSequenceBuilder, \
    ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundSequenceBuilder, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand, IFetchUserGroupsSequenceBuilder, IValidateIfUserBelongsToAtLeastOneGroupCommand, \
    IValidateIfGroupBelongsToUser, IFetchGroupByIdCommand, IGetUserGroupByIdSequenceBuilder, ISetFlatRequestCommand, \
    ICreateFlatCommand, ICreateFlatSequenceBuilder, IValidateFlatRequestCommand, IDeleteFlatCommand, \
    IDeleteFlatSequenceBuilder, IAddCurrentUserToFlatCommand
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, CreateGroupAsyncCommand, \
    UpsertGroupBackgroundCommand, CreateUserGroupsAsyncCommand, UpsertUserGroupsBackgroundCommand, \
    FetchUserGroupsCommand, ValidateIfUserBelongsToAtLeastOneGroupCommand, ValidateIfGroupBelongsToUser, \
    FetchGroupByIdCommand, SetFlatRequestCommand, CreateFlatCommand, ValidateFlatRequestCommand, DeleteFlatCommand, \
    AddCurrentUserToFlatCommand
from src.domain.sequence_builders import CreateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder, \
    UpsertUserGroupsBackgroundSequenceBuilder, FetchUserGroupsSequenceBuilder, GetUserGroupByIdSequenceBuilder, \
    CreateFlatSequenceBuilder, DeleteFlatSequenceBuilder


def register_domain_dependencies(container: Container):
    (container.register(service=ISetGroupRequestCommand, implementation=SetGroupRequestCommand)
     .register(service=IValidateGroupCommand, implementation=ValidateGroupCommand)
     .register(service=ICreateGroupAsyncCommand, implementation=CreateGroupAsyncCommand)
     .register(service=ICreateUserGroupsAsyncCommand, implementation=CreateUserGroupsAsyncCommand)
     .register(service=IUpsertGroupBackgroundCommand, implementation=UpsertGroupBackgroundCommand)
     .register(service=IFetchUserGroupsCommand, implementation=FetchUserGroupsCommand)
     .register(service=IUpsertUserGroupsBackgroundCommand, implementation=UpsertUserGroupsBackgroundCommand)
     .register(service=ICreateGroupSequenceBuilder, implementation=CreateGroupSequenceBuilder)
     .register(service=IUpsertGroupBackgroundSequenceBuilder, implementation=UpsertGroupBackgroundSequenceBuilder)
     .register(service=IFetchUserGroupsSequenceBuilder, implementation=FetchUserGroupsSequenceBuilder)
     .register(service=IFetchGroupByIdCommand, implementation=FetchGroupByIdCommand)
     .register(service=ISetFlatRequestCommand, implementation=SetFlatRequestCommand)
     .register(service=ICreateFlatCommand, implementation=CreateFlatCommand)
     .register(service=IDeleteFlatCommand, implementation=DeleteFlatCommand)
     .register(service=IAddCurrentUserToFlatCommand, implementation=AddCurrentUserToFlatCommand)
     .register(service=IValidateFlatRequestCommand, implementation=ValidateFlatRequestCommand)
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
               implementation=DeleteFlatSequenceBuilder))

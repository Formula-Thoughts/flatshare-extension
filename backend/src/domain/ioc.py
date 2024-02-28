from formula_thoughts_web.ioc import Container

from src.core import ISetGroupRequestCommand, IValidateGroupCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateGroupSequenceBuilder, IUpsertGroupBackgroundSequenceBuilder, \
    ICreateUserGroupsAsyncCommand, IUpsertUserGroupsBackgroundSequenceBuilder, IUpsertUserGroupsBackgroundCommand, \
    IFetchUserGroupsCommand
from src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, CreateGroupAsyncCommand, \
    UpsertGroupBackgroundCommand, CreateUserGroupsAsyncCommand, UpsertUserGroupsBackgroundCommand, \
    FetchUserGroupsCommand
from src.domain.sequence_builders import CreateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder, \
    UpsertUserGroupsBackgroundSequenceBuilder


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
     .register(service=IUpsertUserGroupsBackgroundSequenceBuilder, implementation=UpsertUserGroupsBackgroundSequenceBuilder))

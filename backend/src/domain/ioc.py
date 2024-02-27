from formula_thoughts_web.ioc import Container

from backend.src.core import ISetGroupRequestCommand, IValidateGroupCommand, ICreateGroupAsyncCommand, \
    IUpsertGroupBackgroundCommand, ICreateGroupSequenceBuilder, IUpsertGroupBackgroundSequenceBuilder
from backend.src.domain.commands import SetGroupRequestCommand, ValidateGroupCommand, CreateGroupAsyncCommand, \
    UpsertGroupBackgroundCommand
from backend.src.domain.sequence_builders import CreateGroupSequenceBuilder, UpsertGroupBackgroundSequenceBuilder


def register_domain_dependencies(container: Container):
    (container.register(service=ISetGroupRequestCommand, implementation=SetGroupRequestCommand)
     .register(service=IValidateGroupCommand, implementation=ValidateGroupCommand)
     .register(service=ICreateGroupAsyncCommand, implementation=CreateGroupAsyncCommand)
     .register(service=IUpsertGroupBackgroundCommand, implementation=UpsertGroupBackgroundCommand)
     .register(service=ICreateGroupSequenceBuilder, implementation=CreateGroupSequenceBuilder)
     .register(service=IUpsertGroupBackgroundSequenceBuilder, implementation=UpsertGroupBackgroundSequenceBuilder))
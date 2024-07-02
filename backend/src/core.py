import typing
import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Protocol

from formula_thoughts_web.abstractions import SequenceBuilder, Command

TData = typing.TypeVar("TData")


def uuid4_str():
    return str(uuid.uuid4())


GroupParticipantName = str
GroupId = str
UserId = str
PropertyId = str


@dataclass(unsafe_hash=True)
class Entity:
    etag: str = None
    partition_key: str = None


@dataclass(unsafe_hash=True)
class Property(Entity):
    id: str = field(default_factory=uuid4_str)
    url: str = None
    title: str = None
    price: Decimal = None
    full_name: str = None


@dataclass(unsafe_hash=True)
class UserGroups(Entity):
    id: GroupParticipantName = None
    name: str = None
    groups: list[GroupId] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class Group(Entity):
    id: str = field(default_factory=uuid4_str)
    participants: list[GroupParticipantName] = field(default_factory=lambda: [])
    price_limit: Decimal = None
    locations: list[str] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class GroupProperties(Group):
    properties: list[Property] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class UpsertGroupRequest:
    price_limit: Decimal = None
    locations: list[str] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class CreatePropertyRequest:
    price: Decimal = None
    title: str = None
    url: str = None


class IGroupRepo(Protocol):
    def create(self, group: Group) -> None:
        ...

    def update(self, group: Group) -> None:
        ...

    def get(self, _id: str) -> GroupProperties:
        ...

    def add_participant(self, participant: GroupParticipantName, group: Group) -> None:
        ...


class IPropertyRepo(Protocol):
    def create(self, group_id: GroupId, property: Property) -> None:
        ...

    def delete(self, group_id: GroupId, property_id: PropertyId) -> None:
        ...


class IUserGroupsRepo(Protocol):
    def create(self, user_groups: UserGroups) -> None:
        ...

    def add_group(self, user_groups: UserGroups, group: GroupId) -> None:
        ...

    def get(self, _id: str) -> UserGroups:
        ...


class ISetGroupRequestCommand(Command, Protocol):
    pass


class IValidateGroupCommand(Command, Protocol):
    pass


class IUpdateGroupAsyncCommand(Command, Protocol):
    pass


class ICreateGroupAsyncCommand(Command, Protocol):
    pass


class ICreateGroupCommand(Command, Protocol):
    pass


class ICreateUserGroupsAsyncCommand(Command, Protocol):
    pass


class ICreateUserGroupsCommand(Command, Protocol):
    pass


class IUpsertGroupBackgroundCommand(Command, Protocol):
    pass


class IUpsertUserGroupsBackgroundCommand(Command, Protocol):
    pass


class IValidateIfUserBelongsToAtLeastOneGroupCommand(Command, Protocol):
    pass


class IValidateIfGroupBelongsToUserCommand(Command, Protocol):
    pass


class IFetchAuthUserClaimsIfUserDoesNotExistCommand(Command, Protocol):
    pass


class IFetchUserGroupsCommand(Command, Protocol):
    pass


class IFetchGroupByIdCommand(Command, Protocol):
    pass


class ISetPropertyRequestCommand(Command, Protocol):
    pass


class IValidatePropertyRequestCommand(Command, Protocol):
    pass


class ICreatePropertyCommand(Command, Protocol):
    pass


class IDeletePropertyCommand(Command, Protocol):
    pass


class IAddCurrentUserToGroupCommand(Command, Protocol):
    pass


class ISetGroupIdFromCodeCommand(Command, Protocol):
    pass


class IGetCodeFromGroupIdCommand(Command, Protocol):
    pass


class IUpdateGroupCommand(Command, Protocol):
    pass


class IValidateUserIsNotParticipantCommand(Command, Protocol):
    pass


class IGetCodeForGroupSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpdateGroupSequenceBuilder(SequenceBuilder, Protocol):
    pass


class ICreateGroupSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IFetchUserGroupsSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IGetUserGroupByIdSequenceBuilder(SequenceBuilder, Protocol):
    pass


class ICreatePropertySequenceBuilder(SequenceBuilder, Protocol):
    pass


class IDeletePropertySequenceBuilder(SequenceBuilder, Protocol):
    pass


class IAddUserToGroupSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpsertGroupBackgroundSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpsertUserGroupsBackgroundSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IFetchUserGroupIfExistsSequenceBuilder(SequenceBuilder, Protocol):
    pass
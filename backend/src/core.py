import typing
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from formula_thoughts_web.abstractions import SequenceBuilder, Command

TData = typing.TypeVar("TData")


def uuid4_str():
    return str(uuid.uuid4())


GroupParticipantName = str
GroupId = str
UserId = str
RedFlagId = str
PropertyId = str
PropertyUrl = str


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
    added_by: str = None


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
class AnonymousRedFlag(Entity):
    """
    response model to anonymize the other voters
    """
    id: str = None
    body: str = None
    property_url: str = None
    votes: int = None
    voted_by_me: bool = None
    date: datetime = None


@dataclass(unsafe_hash=True)
class RedFlag(Entity):
    id: str = field(default_factory=uuid4_str)
    body: str = None
    property_url: str = None
    votes: list[UserId] = field(default_factory=lambda: [])
    date: datetime = None


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


@dataclass(unsafe_hash=True)
class CreateRedFlagRequest:
    body: str = None
    property_url: str = None


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


class IRedFlagRepo(Protocol):

    def create(self, red_flag: RedFlag) -> None:
        ...

    def get_by_url(self, property_url: PropertyUrl) -> list[RedFlag]:
        ...

    def get(self, property_url: PropertyUrl, _id: RedFlagId) -> RedFlag:
        ...

    def add_voter(self, user_id: UserId, red_flag: RedFlag) -> None:
        ...

    def remove_voter(self, user_id: UserId, red_flag: RedFlag) -> None:
        ...


class ISetGroupRequestCommand(Command, Protocol):
    pass


class IValidateGroupCommand(Command, Protocol):
    pass


class ICreateGroupCommand(Command, Protocol):
    pass


class ICreateUserGroupsCommand(Command, Protocol):
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


class ICreateRedFlagCommand(Command, Protocol):
    pass


class ISetCreatedAnonymousRedFlagCommand(Command, Protocol):
    pass


class ISetRedFlagRequestCommand(Command, Protocol):
    pass


class IValidateRedFlagRequestCommand(Command, Protocol):
    pass


class IValidatePropertyUrlCommand(Command, Protocol):
    pass


class IGetRedFlagsCommand(Command, Protocol):
    pass


class ISetAnonymousRedFlagsCommand(Command, Protocol):
    pass


class IGetRedFlagByIdCommand(Command, Protocol):
    pass


class ISetAnonymousRedFlagCommand(Command, Protocol):
    pass


class IValidateAlreadyVotedCommand(Command, Protocol):
    pass


class IValidateNotVotedCommand(Command, Protocol):
    pass


class ICreateVoteCommand(Command, Protocol):
    pass


class IDeleteVoteCommand(Command, Protocol):
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


class IFetchUserGroupIfExistsSequenceBuilder(SequenceBuilder, Protocol):
    pass


class ICreateRedFlagSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IGetRedFlagsSequenceBuilder(SequenceBuilder, Protocol):
    pass


class ICreateVoteForRedFlagSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IDeleteVoteForRedFlagSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IValidatePropertyUrlRequestSequenceBuilder(SequenceBuilder, Protocol):
    pass

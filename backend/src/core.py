import typing
import uuid
from dataclasses import dataclass, field
from typing import Protocol

from formula_thoughts_web.abstractions import SequenceBuilder, Command

TData = typing.TypeVar("TData")


def uuid4_str():
    return str(uuid.uuid4())


@dataclass(unsafe_hash=True)
class Flat:
    id: str = field(default_factory=uuid4_str)
    url: str = None
    price: float = None


GroupParticipantAuthId = str
GroupId = str


@dataclass(unsafe_hash=True)
class UserGroups:
    auth_user_id: GroupParticipantAuthId = None
    groups: list[GroupId] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class Group:
    id: str = field(default_factory=uuid4_str)
    flats: list[Flat] = field(default_factory=lambda: [])
    participants: list[GroupParticipantAuthId] = field(default_factory=lambda: [])
    price_limit: float = None
    location: str = None


@dataclass(unsafe_hash=True)
class UpsertGroupRequest:
    price_limit: float = None
    location: str = None


class IBlobRepo(Protocol):
    def create(self, data: TData, key_gen: typing.Callable[[TData], str]) -> None:
        ...


class IGroupRepo(Protocol):
    def create(self, group: Group) -> None:
        ...


class IUserGroupsRepo(Protocol):
    def create(self, user_groups: UserGroups) -> None:
        ...


class ISetGroupRequestCommand(Command, Protocol):
    pass


class IValidateGroupCommand(Command, Protocol):
    pass


class ICreateGroupAsyncCommand(Command, Protocol):
    pass


class ICreateUserGroupsAsyncCommand(Command, Protocol):
    pass


class IUpsertGroupBackgroundCommand(Command, Protocol):
    pass


class IUpsertUserGroupsBackgroundCommand(Command, Protocol):
    pass


class IFetchUserGroupsCommand(SequenceBuilder, Protocol):
    pass


class ICreateGroupSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IFetchUserGroupsSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpsertGroupBackgroundSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpsertUserGroupsBackgroundSequenceBuilder(SequenceBuilder, Protocol):
    pass

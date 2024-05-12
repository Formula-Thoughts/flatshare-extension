import typing
import uuid
from dataclasses import dataclass, field
from typing import Protocol

from formula_thoughts_web.abstractions import SequenceBuilder, Command

TData = typing.TypeVar("TData")


def uuid4_str():
    return str(uuid.uuid4())


GroupParticipantName = str
GroupId = str


@dataclass(unsafe_hash=True)
class Entity:
    etag: str = None
    partition_key: str = None


@dataclass(unsafe_hash=True)
class Property(Entity):
    id: str = field(default_factory=uuid4_str)
    url: str = None
    title: str = None
    price: float = None
    full_name: str = None


@dataclass(unsafe_hash=True)
class UserGroups(Entity):
    id: GroupParticipantName = None
    name: str = None
    groups: list[GroupId] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class Group(Entity):
    id: str = field(default_factory=uuid4_str)
    properties: list[Property] = field(default_factory=lambda: [])
    participants: list[GroupParticipantName] = field(default_factory=lambda: [])
    price_limit: float = None
    locations: list[str] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class UpsertGroupRequest:
    price_limit: float = None
    locations: list[str] = field(default_factory=lambda: [])


@dataclass(unsafe_hash=True)
class CreateFlatRequest:
    price: float = None
    title: str = None
    url: str = None


class IBlobRepo(Protocol):
    def create(self, data: TData, key_gen: typing.Callable[[TData], str]) -> None:
        ...

    def get(self, key: str, model_type: typing.Type[TData]) -> TData:
        ...


class IGroupRepo(Protocol):
    def create(self, group: Group) -> None:
        ...

    def get(self, _id: str) -> Group:
        ...

    def add_participant(self, participant: GroupParticipantName) -> Group:
        ...


class IPropertyRepo(Protocol):
    def create(self, flat: Property) -> None:
        ...


class IUserGroupsRepo(Protocol):
    def create(self, user_groups: UserGroups) -> None:
        ...

    def add_group(self, group: GroupId) -> None:
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


class ICreateUserGroupsAsyncCommand(Command, Protocol):
    pass


class IUpsertGroupBackgroundCommand(Command, Protocol):
    pass


class IUpsertUserGroupsBackgroundCommand(Command, Protocol):
    pass


class IValidateIfUserBelongsToAtLeastOneGroupCommand(Command, Protocol):
    pass


class IValidateIfGroupBelongsToUser(Command, Protocol):
    pass


class IFetchAuthUserClaimsIfUserDoesNotExistCommand(Command, Protocol):
    pass


class IFetchUserGroupsCommand(Command, Protocol):
    pass


class IFetchGroupByIdCommand(Command, Protocol):
    pass


class ISetFlatRequestCommand(Command, Protocol):
    pass


class IValidateFlatRequestCommand(Command, Protocol):
    pass


class ICreateFlatCommand(Command, Protocol):
    pass


class IDeleteFlatCommand(Command, Protocol):
    pass


class IAddCurrentUserToGroupCommand(Command, Protocol):
    pass


class ISetGroupIdFromCodeCommand(Command, Protocol):
    pass


class IGetCodeFromGroupIdCommand(Command, Protocol):
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


class ICreateFlatSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IDeleteFlatSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IAddUserToGroupSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpsertGroupBackgroundSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IUpsertUserGroupsBackgroundSequenceBuilder(SequenceBuilder, Protocol):
    pass


class IFetchUserGroupIfExistsSequenceBuilder(SequenceBuilder, Protocol):
    pass

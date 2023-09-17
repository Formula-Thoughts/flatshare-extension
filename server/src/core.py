import typing
from typing import Protocol

from server.src.domain.models import Group, Resource

T = typing.TypeVar("T")


class RepoBase(Protocol[T]):

    def create(self, data: Resource) -> None:
        ...

    def get_all(self) -> list[T]:
        ...

    def get_by_id(self, _id: str) -> T:
        ...

    def delete_by_id(self, _id: str) -> None:
        ...


class GroupRepo(RepoBase[Group]):
    ...

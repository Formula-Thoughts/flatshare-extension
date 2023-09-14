import typing
from typing import Protocol

from server.src.domain.models import Group

T = typing.TypeVar("T")


class S3BlobRepoBase(Protocol[T]):

    def create(self, data: T) -> None:
        print(str(T))

    def get_all(self) -> list[T]:
        ...

    def get_by_id(self, _id: str) -> T:
        ...

    def delete_by_id(self, _id: str) -> None:
        ...


class GroupRepo(S3BlobRepoBase[Group]):
    ...

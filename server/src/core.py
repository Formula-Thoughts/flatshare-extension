import typing
from typing import Protocol

T = typing.TypeVar("T")


class BlobDataRepo(Protocol[T]):

    def create(self, data: T) -> None:
        ...

    def get_all(self) -> list[T]:
        ...

    def get_by_id(self, _id: str) -> T:
        ...
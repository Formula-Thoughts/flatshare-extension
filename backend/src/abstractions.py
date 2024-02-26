import typing
import uuid
from dataclasses import dataclass, field
from typing import Protocol

from backend.src.domain.models import Group

T = typing.TypeVar("T")


class BlobRepo(Protocol[T]):
    def create(self, data: T, key_gen: typing.Callable[[T], str]) -> None:
        ...


class GroupRepo(Protocol[T]):
    def create(self, data: Group) -> None:
        ...


def uuid4_str():
    return str(uuid.uuid4())


@dataclass(unsafe_hash=True)
class Flat:
    id: str = field(default_factory=uuid4_str)
    url: str = None
    price: float = None


@dataclass(unsafe_hash=True)
class Group:
    code: int = None
    flats: list[Flat] = field(default_factory=lambda: [])

    def can_add_flat(self, flat: Flat) -> bool:
        ...
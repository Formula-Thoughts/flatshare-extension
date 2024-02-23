import typing
from typing import Protocol

from backend.src.domain.models import Group

T = typing.TypeVar("T")


class BlobRepo(Protocol[T]):
    def create(self, data: T, key_gen: typing.Callable[[T], str]) -> None:
        ...


class GroupRepo(Protocol[T]):
    def create(self, data: Group) -> None:
        ...


class Serializer(Protocol):
    def serialize(self, data: typing.Union[dict, list]) -> str:
        ...


class Deserializer(Protocol):
    def deserialize(self, data: str) -> typing.Union[dict, list]:
        ...


class Logger(Protocol):
    def log_error(self, message: str):
        ...

    def log_exception(self, exception: Exception):
        ...

    def log_info(self, message: str):
        ...

    def log_debug(self, message: str):
        ...

    def log_trace(self, message: str):
        ...

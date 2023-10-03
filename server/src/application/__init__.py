from dataclasses import dataclass, field
from typing import Protocol


@dataclass(unsafe_hash=True)
class Response:
    body: dict = None
    status_code: int = None


@dataclass(unsafe_hash=True)
class Error:
    msg: str = None
    status_code: int = None


@dataclass(unsafe_hash=True)
class ServiceContext:
    body: dict = None
    error_capsules: list[Error] = field(default_factory=lambda: [])
    response: Response = None


class Command(Protocol):

    def run(self, context: ServiceContext) -> None:
        ...

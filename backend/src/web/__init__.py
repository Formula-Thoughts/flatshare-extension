from dataclasses import dataclass, field
from typing import Union


@dataclass(unsafe_hash=True)
class Error:
    status: int = None
    message: str = None


@dataclass(unsafe_hash=True)
class Response:
    status: int = None
    body: Union[dict, list] = None


class WebContext:
    response: Response = None,
    short_circuit: bool = False,
    event: Union[list, dict] = field(default_factory=dict),
    body: dict = field(default_factory=dict)
    error_capsule: list[Error] = field(default_factory=list)

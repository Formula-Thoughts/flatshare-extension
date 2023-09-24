import uuid
from dataclasses import dataclass, field


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

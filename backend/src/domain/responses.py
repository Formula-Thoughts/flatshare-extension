from dataclasses import dataclass

from src.core import Group


@dataclass(unsafe_hash=True)
class CreatedGroupResponse(Group):
    pass

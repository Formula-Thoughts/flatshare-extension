from dataclasses import dataclass

from src.core import Group


@dataclass(unsafe_hash=True)
class CreatedGroupResponse:
    group: Group = None


@dataclass(unsafe_hash=True)
class ListUserGroupsResponse:
    groups: list[Group] = None

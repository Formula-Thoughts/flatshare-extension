from dataclasses import dataclass

from src.core import Group, GroupProperties


@dataclass(unsafe_hash=True)
class GetGroupCodeResponse:
    code: str = None


@dataclass(unsafe_hash=True)
class CreatedGroupResponse:
    group: Group = None


@dataclass(unsafe_hash=True)
class SingleGroupResponse:
    group: Group = None


@dataclass(unsafe_hash=True)
class ListUserGroupsResponse:
    groups: list[GroupProperties] = None

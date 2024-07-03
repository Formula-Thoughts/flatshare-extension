from dataclasses import dataclass

from src.core import Group, GroupProperties, Property, AnonymousRedFlag


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
class PropertyCreatedResponse:
    property: Property = None


@dataclass(unsafe_hash=True)
class SingleGroupPropertiesResponse:
    group_properties: GroupProperties = None


@dataclass(unsafe_hash=True)
class ListUserGroupsResponse:
    group_properties_list: list[GroupProperties] = None


@dataclass(unsafe_hash=True)
class SingleRedFlagResponse:
    red_flag: AnonymousRedFlag = None


@dataclass(unsafe_hash=True)
class CreatedRedFlagResponse:
    red_flag: AnonymousRedFlag = None


@dataclass(unsafe_hash=True)
class ListRedFlagsResponse:
    red_flags: list[AnonymousRedFlag] = None

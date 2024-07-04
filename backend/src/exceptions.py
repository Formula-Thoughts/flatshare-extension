class UserGroupsNotFoundException(Exception):
    pass


class GroupNotFoundException(Exception):
    pass


class PropertyNotFoundException(Exception):
    pass


class GroupAlreadyExistsException(Exception):
    pass


class UserGroupAlreadyExistsException(Exception):
    pass


class ConflictException(Exception):
    pass


class DataException(Exception):
    pass


class RedFlagAlreadyExistsException(Exception):
    pass
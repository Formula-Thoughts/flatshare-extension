from formula_thoughts_web.abstractions import Error


class InvalidGroupError(Error):
    ...


class UserGroupsNotFoundError(Error):
    ...


class GroupNotFoundError(Error):
    ...


invalid_price_error = InvalidGroupError(message="price has to be greater than 0")

invalid_locations_error = InvalidGroupError(message="a group must have 1 or more locations")

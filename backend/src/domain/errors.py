from formula_thoughts_web.abstractions import Error


class InvalidGroupDataError(Error):
    ...


class UserGroupsNotFoundError(Error):
    ...


class GroupNotFoundError(Error):
    ...


class FlatNotFoundError(Error):
    ...


current_user_already_added_to_group = InvalidGroupDataError(message="current user already added to group")

invalid_price_error = InvalidGroupDataError(message="price has to be greater than 0")

invalid_group_locations_error = InvalidGroupDataError(message="a group must have 1 or more locations")

invalid_flat_price_error = InvalidGroupDataError(message="price has to be less than the group's price limit")

invalid_flat_location_error = InvalidGroupDataError(message="flat's location is not accepted by the group")

code_required_error = InvalidGroupDataError(message="code parameter is required from group invite")

user_already_part_of_group_error = InvalidGroupDataError(message="user is already added to group")

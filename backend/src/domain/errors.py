from formula_thoughts_web.abstractions import Error


class InvalidGroupDataError(Error):
    ...


class UserGroupsNotFoundError(Error):
    ...


class GroupNotFoundError(Error):
    ...


class PropertyNotFoundError(Error):
    ...


current_user_already_added_to_group = InvalidGroupDataError(message="current user already added to group")

invalid_price_error = InvalidGroupDataError(message="price has to be greater than 0")

property_price_required_error = InvalidGroupDataError(message="price field is a required attribute")

property_url_required_error = InvalidGroupDataError(message="url field is a required attribute")

property_title_required_error = InvalidGroupDataError(message="title field is a required attribute")

code_required_error = InvalidGroupDataError(message="code parameter is required from group invite")

user_already_part_of_group_error = InvalidGroupDataError(message="user is already added to group")

from formula_thoughts_web.abstractions import Error


class InvalidGroupDataError(Error):
    ...


class InvalidPropertyDataError(Error):
    ...


class UserGroupsNotFoundError(Error):
    ...


class GroupNotFoundError(Error):
    ...


class PropertyNotFoundError(Error):
    ...


class RedFlagNotFoundError(Error):
    ...


class InvalidRedFlagDataError(Error):
    ...


class InvalidVotingStatusError(Error):
    ...


current_user_already_added_to_group = InvalidGroupDataError(message="current user already added to group")

invalid_price_error = InvalidGroupDataError(message="price has to be greater than 0")

property_price_required_error = InvalidPropertyDataError(message="price field is a required attribute")

property_url_required_error = InvalidPropertyDataError(message="url field is a required attribute")

property_title_required_error = InvalidPropertyDataError(message="title field is a required attribute")

code_required_error = InvalidGroupDataError(message="code parameter is required from group invite")

user_already_part_of_group_error = InvalidGroupDataError(message="user is already added to group")

user_not_part_of_group_error = InvalidGroupDataError(message="user is not added to group")

red_flag_property_url_required_error = InvalidRedFlagDataError(message="property url field is a required attribute")

red_flag_property_url_param_required_error = InvalidRedFlagDataError(message="property url parameter is required")

red_flag_body_required_error = InvalidRedFlagDataError(message="body field is a required attribute")

user_has_already_voted_error = InvalidVotingStatusError(message="current user has already voted")

user_has_not_voted_error = InvalidVotingStatusError(message="current user has not voted")

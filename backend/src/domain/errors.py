from formula_thoughts_web.abstractions import Error


class InvalidGroupError(Error):
    ...


class UserGroupsNotFoundError(Error):

    def __init__(self, auth_user_id: str):
        self.message = f"User groups not found for user: {auth_user_id}"


invalid_price_error = InvalidGroupError(message="price has to be greater than 0")
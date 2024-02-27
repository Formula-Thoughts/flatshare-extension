from formula_thoughts_web.abstractions import Error


class InvalidGroupError(Error):
    ...


invalid_price_error = InvalidGroupError(message="price has to be greater than 0")
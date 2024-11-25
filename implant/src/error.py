class RequestError(Exception):
    pass


class MethodError(RequestError):
    pass


class CommandError(Exception):
    pass
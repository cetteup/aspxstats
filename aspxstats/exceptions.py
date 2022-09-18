class Error(Exception):
    pass


class ClientError(Error):
    pass


class InvalidResponseError(Error):
    pass


class NotFoundError(Error):
    pass


class InvalidParameterError(Error):
    pass

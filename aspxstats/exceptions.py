from typing import Optional, Any


class Error(Exception):
    pass


class ClientError(Error):
    pass


class TimeoutError(Error):
    pass


class InvalidResponseError(Error):
    path: Optional[str]
    attribute: Optional[Any]

    def __init__(self, message: str, path: Optional[str] = None, attribute: Optional[Any] = None):
        super().__init__(message)
        self.path = path
        self.attribute = attribute

    def __str__(self) -> str:
        if self.path is not None and self.attribute is not None:
            return f'{super().__str__()}: {self.path}={self.attribute}'

        return super().__str__()


class NotFoundError(Error):
    pass


class InvalidParameterError(Error):
    pass

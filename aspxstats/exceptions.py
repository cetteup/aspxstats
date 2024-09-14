from typing import Optional, Any


class Error(Exception):
    pass


class ClientError(Error):
    pass


class TimeoutError(Error):
    pass


class InvalidResponseError(Error):
    pass


class ValidationError(Error):
    path: str
    value: Optional[Any]

    def __init__(self, path: str, attribute: Optional[Any] = None):
        self.path = path
        self.value = attribute

    def __str__(self) -> str:
        if self.value is not None:
            return 'Received response contains invalid attribute value: ' + '='.join([self.path, str(self.value)])

        return 'Received response is missing attribute: ' + self.path

class NotFoundError(Error):
    pass


class InvalidParameterError(Error):
    pass

class OplusClientError(Exception):
    pass


class HttpClientError(OplusClientError):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class HttpServerError(OplusClientError):
    pass


class RecordNotFoundError(OplusClientError):
    pass


class MultipleRecordsFoundError(OplusClientError):
    pass


class InvalidToken(OplusClientError):
    pass


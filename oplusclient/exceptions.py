class OplusClientError(Exception):
    pass


class HttpClientError(OplusClientError):
    pass


class HttpServerError(OplusClientError):
    pass


class RecordNotFoundError(OplusClientError):
    pass


class MultipleRecordsFoundError(OplusClientError):
    pass


class InvalidToken(OplusClientError):
    pass


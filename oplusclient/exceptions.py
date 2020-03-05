class OplusClientError(Exception):
    pass


class RecordNotFoundError(OplusClientError):
    pass


class MultipleRecordsFoundError(OplusClientError):
    pass


class InvalidToken(OplusClientError):
    pass


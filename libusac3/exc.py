class USACError(BaseException):
    pass


class CSVNotFoundError(USACError):
    pass


class CSVParseError(USACError):
    pass
from src.exceptions.rebate_exception import RebateException


class IntegrityExceptions(RebateException):
    def __init__(self, message,
                 code=None, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)


class ValidationsExceptions(RebateException):
    def __init__(self, message,
                 code=None, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)


class NotFoundException(RebateException):
    def __init__(self, message,
                 code=404, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)

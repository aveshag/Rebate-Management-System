from src.exceptions.rebate_exception import RebateException


class DBException(RebateException):
    def __init__(self, message,
                 code=None, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)

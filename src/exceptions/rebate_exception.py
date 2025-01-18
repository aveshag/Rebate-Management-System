class RebateException(Exception):

    def __init__(self, message: str, code, *args, **kwargs):
        """
        Initialize the exception with a message and an optional code.

        :param message: The error message.
        :param code: An optional error code. Default is 500.
        """
        super().__init__(message, *args)
        self.message = message
        self.code = code if code else 400
        self.extra = kwargs

    def __str__(self):
        """
        Return a string representation of the exception.
        """
        return self.message

    def to_dict(self):
        """
        Convert the exception to a dictionary format for structured output.
        """
        return {
            "message": self.message,
            "code": self.code,
            **self.extra
        }

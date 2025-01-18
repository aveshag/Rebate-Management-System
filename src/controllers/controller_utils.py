import logging

from src.exceptions.rebate_exception import RebateException
from src.utils import get_error_object, get_error_content, create_response

logger = logging.getLogger(__name__)

# Not used
def handle_exception(api_type):
    def inner_decorator(func):
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except RebateException as e:
                logger.exception(
                    f"Exception occurred while API request for {api_type}")
                errors = [get_error_object(str(e))]
                return create_response(
                    get_error_content(errors), e.code)
            except Exception as e:
                logger.exception(
                    f"Unknown exception occurred while API request for {api_type}")
                errors = [get_error_object(str(e))]
                return create_response(get_error_content(errors), 500)

        return wrapper

    return inner_decorator

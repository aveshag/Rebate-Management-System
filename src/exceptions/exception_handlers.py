import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from src.exceptions.rebate_exception import RebateException
from src.utils import get_error_object, get_error_content, create_response

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)
    app.add_exception_handler(RebateException, rebate_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)


def rebate_exception_handler(request: Request, exc: RebateException):
    logger.exception(f"Exception occurred while handling request "
                     f"{request.method} {request.url.path}", exc_info=exc)
    errors = [get_error_object(str(exc))]
    return create_response(get_error_content(errors), exc.code)


def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unknown exception occurred while handling request "
                     f"{request.method} {request.url.path}", exc_info=exc)
    errors = [get_error_object(str(exc))]
    return create_response(get_error_content(errors), 500)


def validation_exception_handler(request: Request,
                                 exc: RequestValidationError):
    errors = [
        get_error_object(f"{error['loc'][-1]}: {error['msg']}")
        for error in exc.errors()
    ]
    return create_response((get_error_content(errors)), 422)

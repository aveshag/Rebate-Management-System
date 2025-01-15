from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.routes.api_models import ErrorDetail, ErrorResponse


def register_exception_handlers(app):
    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)


def validation_exception_handler(request: Request,
                                 exc: RequestValidationError):
    errors = [
        ErrorDetail(message=f"{error['loc'][-1]}: {error['msg']}")
        for error in exc.errors()
    ]
    error_response = ErrorResponse(
        errors=errors
    )
    return JSONResponse(status_code=422, content=error_response.model_dump())

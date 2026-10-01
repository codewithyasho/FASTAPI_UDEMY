from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation failed in field 'rating'",
            "details": "Rating must be between 1 and 5"
        }
    )

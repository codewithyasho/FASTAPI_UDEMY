from fastapi.responses import JSONResponse
from fastapi import Request

## CUSTOM EXCEPTIONS ##


class PinCodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class InvalidPinCodeError(Exception):
    def __init__(self, pincode: str, reason: str = "Invalid Format"):
        self.pincode = pincode
        self.reason = reason


## CUSTOM ERROR HANDLERS ##

async def pincode_not_found_handler(request: Request, exception: PinCodeNotFoundError):

    return JSONResponse(
        status_code=404,
        content={
            "error": "pincode_not_found",
            "message": f"No locations found for this pincode: {exception.pincode}",
            "pincode": exception.pincode
        }
    )


async def invalid_pincode_handler(request: Request, exception: InvalidPinCodeError):

    return JSONResponse(
        status_code=400,
        content={
            "error": f"invalid_pincode '{exception.pincode}'",
            "message": f"Please enter the correct pincode",
            "reason": exception.reason
        }
    )

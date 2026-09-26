from fastapi import FastAPI
import uvicorn
from exceptions import PinCodeNotFoundError, pincode_not_found_handler, InvalidPinCodeError, invalid_pincode_handler
from models import PincodeRequest, PincodeResponse, BulkResquest, BulkResponse
from data import pincode_db

app = FastAPI(
    title="Pincode Lookup API",
    description="Auto fill city and state from indian pincode during checkout"
)


# register your custom exception handlers
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Pincode lookup api",
        "status": "healthy"
    }


# if it is a get request, we will send the pincode in the url path.
# so we will use path parameter to get the pincode from the url.
@app.get("/pincode/{code}", response_model=PincodeResponse)
def pincode_lookup(code: str):
    if len(code) != 6 or not code.isdigit():
        raise PinCodeNotFoundError(code)

    if code not in pincode_db:
        raise PinCodeNotFoundError(code)

    return pincode_db[code]


# whenever sending the post request, 
# we will send the data in json format in the body of the request.
@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_pincode_lookup(request: BulkResquest):
    restults = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            restults.append(pincode_db[code])
        else:
            missing.append(code)

    return BulkResponse(
        found=len(restults),
        results=restults,
        not_found=len(missing),
        missing=missing
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

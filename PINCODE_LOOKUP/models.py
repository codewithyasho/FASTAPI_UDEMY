from pydantic import BaseModel, field_validator


class PincodeRequest(BaseModel):
    pincode: str

    # pincode must be excatly 6 digits only

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Pincode must be exaclty 6 digits")
        return value


class PincodeResponse(BaseModel):
    status: str = "success"
    pincode: str
    city: str
    state: str
    district: str


class BulkResquest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError("Atleast 1 pincode is required")

        if len(values) > 20:
            raise ValueError("Maximun 20 pincodes allowed per request")

        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError("Each Pincode must be exaclty 6 digits")
            return values


class BulkResponse(BaseModel):
    status: str = "success"

    found: int
    results: list[PincodeResponse]

    not_found: int
    missing: list[str]

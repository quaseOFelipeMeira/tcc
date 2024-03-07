from pydantic import BaseModel
from typing import Optional
from datetime import date


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class LoginSchema(BaseModel):
    email: str
    password: str


class descSchema(BaseModel):
    desc: str


class descResponseSchema(descSchema):
    id: int


class productTypeSchema(BaseModel):
    desc: str
    cost_center: str


class productTypeResponseSchema(productTypeSchema):
    id: int


class toolingSchema(BaseModel):
    project: str
    client_supplier: str
    part_number: str
    RBSNO: str

    price: float

    request_type: int
    product_type: int
    tooling_type: int
    # requested_by: int

    date_request: date
    date_sop: date


class toolingResponseSchema(toolingSchema):
    was_approved: Optional[bool] = None
    status_description: Optional[str] = None
    date_input: date
    date_request: date


class partNumberSchema(BaseModel):
    part_number: str


class statusSchema(BaseModel):
    status: bool
    status_description: Optional[str] = None

from pydantic import BaseModel
from typing import Optional, List
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


class RequestType(BaseModel):
    desc:str
    
class ProductType(BaseModel):
    desc:str
    cost_center:str
    
class ToolingType(BaseModel):
    desc:str

class toolingSchema(BaseModel):
    project: str
    client_supplier: int
    part_number: str
    RBSNO: str

    price: float

    request: RequestType
    product: ProductType
    tooling_t: ToolingType

    date_request: date
    date_sop: date


class toolingResponseSchema(toolingSchema):
    id: int
    was_approved: Optional[bool] = None
    status_description: Optional[str] = None
    date_input: date
    date_request: date


class toolingWithHistoric(toolingResponseSchema):
    history: Optional[List[toolingResponseSchema]]


class partNumberSchema(BaseModel):
    part_number: str


class statusSchema(BaseModel):
    status: bool
    status_description: Optional[str] = None


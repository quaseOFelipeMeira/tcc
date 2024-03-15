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


class clientSchema(BaseModel):
    name: str


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
    
class DateCFResponse(BaseModel):
    desc:str

class toolingSchema(BaseModel):
    project: str
    client: clientSchema
    part_number: str
    RBSNO: Optional[str] = None
    price: float
    product: ProductType
    tooling_t: ToolingType
    date_request: date
    date_sop: date


class dateCF(BaseModel):
    desc: str
    date_exp: date


class toolingResponseSchema(toolingSchema):
    id: int
    was_approved: Optional[bool] = None
    request: RequestType
    bp: int
    cf: Optional[DateCFResponse] = None
    date_input: date
    date_request: date
    requested_by: str


class toolingResponseUpdateSchema(toolingSchema):
    id: int
    was_approved: Optional[bool] = None
    request: RequestType
    date_input: date
    date_request: date

class toolingWithHistoric(toolingResponseSchema):
    history: Optional[List[toolingResponseUpdateSchema]]


class partNumberSchema(BaseModel):
    part_number: str


class statusSchema(BaseModel):
    status: bool
    status_description: Optional[str] = None


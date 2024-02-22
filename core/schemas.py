from pydantic import BaseModel
from typing import Optional


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
    id:int
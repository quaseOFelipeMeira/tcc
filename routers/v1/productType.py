""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import ProductType
from core.schemas import productTypeSchema, productTypeResponseSchema
from core.exceptions import EXCEPTIONS
from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Product Types"],
    prefix="/productType",
)


@router.get("", response_model=List[productTypeResponseSchema])
def get_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    types = db.query(ProductType).all()
    return types


@router.get("/{id}", response_model=productTypeResponseSchema)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    types = db.query(ProductType).filter(ProductType.id == id).first()

    if not types:
        raise EXCEPTIONS.PRODUCT_TYPE.NOT_FOUND

    return types


@router.post("", response_model=productTypeSchema)
def add(
    request: productTypeSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):

    new_type = ProductType(
        desc=request.desc,
        cost_center=request.cost_center,
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.put("/{id}")
def update(
    id: int,
    request: productTypeSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):

    old_type = db.query(ProductType).filter(ProductType.id == id)
    
    if not old_type:
        raise EXCEPTIONS.PRODUCT_TYPE.NOT_FOUND

    old_type.update(request.model_dump())
    db.commit()
    return request

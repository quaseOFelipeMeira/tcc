""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import RequestType
from core.schemas import descSchema, descResponseSchema

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Request Types"],
    prefix="/requestType",
)


@router.get("", response_model=List[descResponseSchema])
def get_all(db: Session = Depends(get_db), user = Depends(get_current_user_azure)):
    types = db.query(RequestType).all()
    return types


@router.get("/{id}", response_model=descResponseSchema)
def get_by_id(id: int, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):
    types = db.query(RequestType).filter(RequestType.id == id).first()
    return types


@router.post("", response_model=descSchema)
def add(request: descSchema, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):

    new_type = RequestType(
        desc=request.desc,
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.put("/{id}")
def update(id: int, request: descResponseSchema, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):

    old_type = db.query(RequestType).filter(RequestType.id == id)

    if not old_type:
        pass

    old_type.update(request.model_dump())
    db.commit()
    return request


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):

    deleted_type = db.query(RequestType).filter(RequestType.id == id).first()
    if deleted_type:
        db.delete(deleted_type)
        db.commit()
        return {"Type deleted"}
    return {"Not Founded"}

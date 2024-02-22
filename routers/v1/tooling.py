""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Tooling
from core.schemas import toolingSchema, toolingResponseSchema

from datetime import date


router = APIRouter(
    tags=["Tooling"],
    prefix="/tooling",
)


@router.get("", response_model=List[toolingResponseSchema])
def get_all(db: Session = Depends(get_db)):
    types = db.query(Tooling).all()
    return types


@router.get("/{id}", response_model=toolingResponseSchema)
def get_by_id(id: int, db: Session = Depends(get_db)):
    types = db.query(Tooling).filter(Tooling.id == id).first()
    return types


@router.post("", response_model=toolingResponseSchema)
def add(request: toolingSchema, db: Session = Depends(get_db)):

    new_tooling = Tooling(
        project=request.project,
        client_supplier=request.client_supplier,
        part_number=request.part_number,
        price=request.price,
        request_type=request.request_type,
        product_type=request.product_type,
        tooling_type=request.tooling_type,
        requested_by=request.requested_by,
        date_input=date.today(),
        date_request=request.date_request,
        date_sop=request.date_sop,
    )
    db.add(new_tooling)
    db.commit()
    db.refresh(new_tooling)
    return new_tooling


@router.put("/{id}")
def update(id: int, request: toolingSchema, db: Session = Depends(get_db)):

    old_type = db.query(Tooling).filter(Tooling.id == id)
    if not old_type:
        pass

    old_type.update(request.model_dump())
    db.commit()
    return request


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):

    deleted_type = db.query(Tooling).filter(Tooling.id == id).first()
    if deleted_type:
        db.delete(deleted_type)
        db.commit()
        return {"Type deleted"}
    return {"Not Founded"}

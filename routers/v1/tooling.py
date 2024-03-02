""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from core.database import get_db
from core.models import Tooling
from core.schemas import (
    toolingSchema,
    toolingResponseSchema,
    partNumberSchema,
    statusSchema,
)

from datetime import date

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Tooling"],
    prefix="/tooling",
)


def set_status_description(date_to_format: date):
    # Method to return the date status description - BP00CF00
    cf03 = date(date_to_format.year, 3, 1)
    cf05 = date(date_to_format.year, 5, 1)
    cf07 = date(date_to_format.year, 7, 1)

    cf = ""
    if date_to_format.month - cf07.month < 0:
        cf = "07"
    elif date_to_format.month - cf05.month < 0:
        cf = "05"
    elif date_to_format.month - cf03.month < 0:
        cf = "03"
    str_year = str(date_to_format.year)

    return f"BP{str_year[-2]}{str_year[-1]}CF{cf}"


@router.get("")
# async def get_all(db: Session = Depends(get_db), token: str = Header(...), user = None) -> Page[toolingSchema]:
async def get_all(db: Session = Depends(get_db)) -> Page[toolingSchema]:
    return paginate(db, select(Tooling).order_by(Tooling.id))


@router.get("/{id}", response_model=toolingResponseSchema)
def get_by_id(id: int, db: Session = Depends(get_db)):
    types = db.query(Tooling).filter(Tooling.id == id).first()
    return types


@router.post("", response_model=toolingResponseSchema)
def add(request: toolingSchema, db: Session = Depends(get_db), user=None):

    print(user)

    new_tooling = Tooling(
        project=request.project,
        client_supplier=request.client_supplier,
        part_number=request.part_number,
        price=request.price,
        request_type=request.request_type,
        product_type=request.product_type,
        tooling_type=request.tooling_type,
        # requested_by=request.requested_by,
        date_input=date.today(),
        date_request=request.date_request,
        date_sop=request.date_sop,
        RBSNO=request.RBSNO,
        status_description=set_status_description(request.date_sop),
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


@router.patch("/{id}/part-number")
def update_part_number(
    id: int, request: partNumberSchema, db: Session = Depends(get_db)
):
    tooling = db.query(Tooling).filter(Tooling.id == id).first()
    if not tooling:
        pass

    tooling.part_number = request.part_number
    db.commit()
    return request


@router.patch("/{id}/status")
def update_status(id: int, request: statusSchema, db: Session = Depends(get_db)):
    tooling = db.query(Tooling).filter(Tooling.id == id).first()
    if not tooling:
        pass

    tooling.was_approved = request.status
    if request.status == False:
        tooling.status_description = request.status_description
    db.commit()
    db.refresh(tooling)
    return tooling


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):

    deleted_type = db.query(Tooling).filter(Tooling.id == id).first()
    if deleted_type:
        db.delete(deleted_type)
        db.commit()
        return {"Type deleted"}
    return {"Not Founded"}

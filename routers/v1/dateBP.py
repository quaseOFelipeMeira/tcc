""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from core.database import get_db
from core.models import DateBP, DateCF
from core.exceptions import EXCEPTIONS
from core.schemas import (
    datePatchSchema,
    dateResponseSchema,
    bpcfSchema,
    bpcfResponseSchema,
)

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["DateBP"],
    prefix="/dateBP",
)


@router.get("", response_model=Page[bpcfResponseSchema])
def get_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
) -> Page[bpcfResponseSchema]:

    if user.get("roles")[0] != "PPS":
        raise EXCEPTIONS.AUTHORIZATION.NOT_ENOUGH_PERMISSION

    dates = db.query(DateBP).order_by(desc(DateBP.id))
    return paginate(db, dates)


@router.get("/{id}", response_model=dateResponseSchema)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise EXCEPTIONS.AUTHORIZATION.NOT_ENOUGH_PERMISSION

    dateBP = db.query(DateBP).filter(DateBP.id == id).first()

    if not dateBP:
        raise EXCEPTIONS.BP.NOT_FOUND

    return dateBP


@router.post("")
def add(
    request: bpcfSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise EXCEPTIONS.AUTHORIZATION.NOT_ENOUGH_PERMISSION

    BP_desc = str(request.date_bp.year)[2:]

    new_BP = DateBP(
        desc=BP_desc,
        date_exp=request.date_bp,
    )

    db.add(new_BP)
    db.commit()

    last_added_bp = db.query(DateBP).order_by(desc(DateBP.id)).first()

    cf_dates = [
        request.date_cf1,
        request.date_cf2,
        request.date_cf3,
    ]

    for date in cf_dates:

        if date.month < 10:
            name = "0" + str(date.month)
        else:
            name = str(date.month)

        new_CF = DateCF(
            desc=name,
            date_exp=date,
            bp=last_added_bp.id,
        )
        db.add(new_CF)

    db.commit()
    return new_BP


@router.patch("/{id}")
def update_date(
    id: int,
    request: datePatchSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise EXCEPTIONS.AUTHORIZATION.NOT_ENOUGH_PERMISSION

    query = db.query(DateBP).filter(DateBP.id == id)
    cf_to_update = query.first()

    if not cf_to_update:
        raise EXCEPTIONS.BP.NOT_FOUND

    query.update(request.model_dump())
    db.commit()

    return request

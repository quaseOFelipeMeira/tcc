""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import DateCF
from core.schemas import datePatchSchema, dateResponseSchema
from core.exceptions import EXCEPTIONS

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["DateCF"],
    prefix="/dateCF",
)


@router.get("/{id}", response_model=dateResponseSchema)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise EXCEPTIONS.AUTHORIZATION.NOT_ENOUGH_PERMISSION

    dates = db.query(DateCF).filter(DateCF.id == id).first()
    
    if not dates:
        raise EXCEPTIONS.CF.NOT_FOUND
        
    return dates


@router.patch("/{id}")
def update_date(
    id: int,
    request: datePatchSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise EXCEPTIONS.AUTHORIZATION.NOT_ENOUGH_PERMISSION

    query = db.query(DateCF).filter(DateCF.id == id)
    cf_to_update = query.first()

    if not cf_to_update:
        raise EXCEPTIONS.CF.NOT_FOUND

    query.update(request.model_dump())
    db.commit()

    return request

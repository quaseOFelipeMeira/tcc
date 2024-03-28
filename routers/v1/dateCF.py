""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.models import DateCF
from core.schemas import dateSchema, datePatchSchema, dateResponseSchema


from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["DateCF"],
    prefix="/dateCF",
)


# @router.get("", response_model=List[dateResponseSchema])
# def get_all(
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user_azure),
# ):
#     if user.get("roles")[0] != "PPS":
#         raise (
#             HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="You are not authorized to this information",
#             )
#         )

#     dates = db.query(DateCF).all()
#     return dates


@router.get("/{id}", response_model=dateResponseSchema)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise (
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to this information",
            )
        )

    dates = db.query(DateCF).filter(DateCF.id == id).first()
    return dates


# @router.post("", response_model=dateSchema)
# def add(
#     request: dateSchema,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user_azure),
# ):
#     if user.get("roles")[0] != "PPS":
#         raise (
#             HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Você não está autorizado a fazer essa requisição",
#             )
#         )

#     new_dateCF = DateCF(
#         desc=request.desc,
#         date_exp=request.date_exp,
#     )

#     db.add(new_dateCF)
#     db.commit()
#     db.refresh(new_dateCF)
#     return new_dateCF


@router.patch("/{id}")
def update_date(
    id: int,
    request: datePatchSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] != "PPS":
        raise (
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to this information",
            )
        )

    query = db.query(DateCF).filter(DateCF.id == id)
    cf_to_update = query.first()

    if not cf_to_update:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="CF not founded"
            )
        )

    query.update(request.model_dump())
    db.commit()

    return request

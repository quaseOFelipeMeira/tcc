""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import ToolingType
from core.schemas import descSchema, descResponseSchema
from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Tooling Types"],
    prefix="/toolingType",
)


@router.get("", response_model=List[descResponseSchema])
def get_all(db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    types = db.query(ToolingType).all()
    return types


@router.get("/{id}", response_model=descSchema)
def get_by_id(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user_azure)
):
    types = db.query(ToolingType).filter(ToolingType.id == id).first()
    return types


@router.post("", response_model=descSchema)
def add(
    request: descSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):

    new_type = ToolingType(
        desc=request.desc,
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.put("/{id}")
def update(
    id: int,
    request: descSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):

    old_type = db.query(ToolingType).filter(ToolingType.id == id)
    if not old_type:
        pass

    old_type.update(request.model_dump())
    db.commit()
    return request


# @router.delete("/{id}")
# def delete(id: int, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):

#     deleted_type = db.query(ToolingType).filter(ToolingType.id == id).first()
#     if deleted_type:
#         db.delete(deleted_type)
#         db.commit()
#         return {"Type deleted"}
#     return {"Not Founded"}

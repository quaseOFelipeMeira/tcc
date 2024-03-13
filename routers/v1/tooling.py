""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, and_

from core.database import get_db
from core.models import Tooling, RequestType, ToolingUpdates, DateCF, ToolingType, ProductType
from core.schemas import (
    toolingSchema,
    toolingResponseSchema,
    partNumberSchema,
    statusSchema,
    toolingWithHistoric
)

from datetime import date

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Tooling"],
    prefix="/tooling",
)


def set_status_description(request: toolingSchema, db: Session):
    # Method to return the date status description - BP00CF00
    cf03 = db.query(DateCF).filter(DateCF.desc == "03").first()
    cf05 = db.query(DateCF).filter(DateCF.desc == "05").first()
    cf07 = db.query(DateCF).filter(DateCF.desc == "07").first()
        
    if request.date_sop.year > date.today().year:
        return str(request.date_sop.year)[2:], None

    if request.date_request < cf03.date_exp:
        return str(request.date_sop.year)[2:], cf03.id
    elif request.date_request < cf05.date_exp:
        return str(request.date_sop.year)[2:], cf05.id
    elif request.date_request < cf07.date_exp:
        return str(request.date_sop.year)[2:], cf07.id

@router.get("", response_model=Page[toolingResponseSchema])
async def get_all(db: Session = Depends(get_db), user=Depends(get_current_user_azure)) -> Page[toolingSchema]:
    if user.get("roles")[0] == "PPS":
        return paginate(db, select(Tooling).order_by(Tooling.id))
    
    request_type = (db.query(RequestType).filter(RequestType.desc == user.get("roles")[0]).first())
    
    return paginate(db, select(Tooling).filter(Tooling.request_type == request_type.id).order_by(Tooling.id))


@router.get("/{id}", response_model=toolingWithHistoric)
def get_by_id(id: int, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    if user.get("roles")[0] == "PPS":
        tooling = db.query(Tooling).filter(Tooling.id == id).first()
        return tooling
    
    request_type = db.query(RequestType).filter(RequestType.desc == user.get("roles")[0]).first()
    search_tooling = db.query(Tooling).filter(Tooling.id == id).first()
    if search_tooling.request_type == request_type.id:
        return search_tooling
    else:
        raise (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não está autorizado a ver essa informação"))


@router.post("", response_model=toolingResponseSchema)
def add(request: toolingSchema, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    # if user.get("roles")[0] == "PPS":
        # raise(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não está autorizado a fazer essa requisição"))        
    
    tooling_type = db.query(ToolingType).filter_by(desc=request.tooling_t.desc).first()
    product_type = db.query(ProductType).filter_by(desc=request.product.desc).first()
    request_type = db.query(RequestType).filter_by(desc=user.get("roles")[0]).first()

    bp, cf = set_status_description(request, db)
    
    new_tooling = Tooling(
        project=request.project,
        client_supplier=request.client_supplier,
        part_number=request.part_number,
        price=request.price,
        request_type=request_type.id,
        product_type=product_type.id,
        tooling_type=tooling_type.id,
        requested_by=user["oid"],
        date_input=date.today(),
        date_request=request.date_request,
        date_sop=request.date_sop,
        RBSNO=request.RBSNO,
        bp=bp,
        cf_id=cf
    )
    
    db.add(new_tooling)
    db.commit()
    db.refresh(new_tooling)
    
    return new_tooling


@router.put("/{id}")
def update(id: int, request: toolingSchema, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    query = db.query(Tooling).filter(Tooling.id == id)
    tooling = query.first()

    if not tooling:
        pass
    
    if not tooling.requested_by == user['oid']:
        raise(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não está autorizado a fazer essa requisição"))

    tooling_updated = ToolingUpdates(
        tooling_fk=tooling.id,
        project=tooling.project,
        client_supplier=tooling.client_supplier,
        part_number=tooling.part_number,
        price=tooling.price,
        request_type=tooling.request_type,
        product_type=tooling.product_type,
        tooling_type=tooling.tooling_type,
        date_input=tooling.date_input,
        date_request=tooling.date_request,
        date_sop=tooling.date_sop,
        RBSNO=tooling.RBSNO
    )

    db.add(tooling_updated)

    tooling.date_input = date.today()
    query.update(request.model_dump())
    db.commit()
    return request


@router.patch("/{id}/part-number")
def update_part_number(id: int, request: partNumberSchema, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    if not user.get("roles")[0] == "SO":
        raise(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não está autorizado a fazer essa requisição"))
    
    tooling = db.query(Tooling).filter(Tooling.id == id).first()
    
    if not tooling:
        pass

    tooling.part_number = request.part_number
    db.commit()
    return request


@router.patch("/{id}/status")
def update_status(id: int, request: statusSchema, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    if not user.get("roles")[0] == "PPS":
        raise(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não está autorizado a fazer essa requisição"))
    
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
def delete(id: int, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    deleted_type = db.query(Tooling).filter(Tooling.id == id).first()
    if deleted_type:
        db.delete(deleted_type)
        db.commit()
        return {"Type deleted"}
    return {"Not Founded"}

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
from core.models import (
    Tooling,
    RequestType,
    ToolingUpdates,
    ToolingType,
    ProductType,
    Client,
    DateCF,
    DateBP,
)

from core.schemas import (
    toolingSchema,
    toolingResponseSchema,
    partNumberSchema,
    statusSchema,
    toolingWithHistoric,
)

from datetime import date

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Tooling"],
    prefix="/tooling",
)


def set_status_description(request: toolingSchema, db: Session):
    # Method to return the date status description

    cf03 = db.query(DateCF).filter(DateCF.desc == "03").first()
    cf05 = db.query(DateCF).filter(DateCF.desc == "05").first()
    cf07 = db.query(DateCF).filter(DateCF.desc == "07").first()

    str_sop_date = str(request.date_sop.year)[2:]
    bp_id = db.query(DateBP).filter(DateBP.desc == str_sop_date).first().id

    # Condition if the sop date of the tooling is for the next year
    if request.date_sop.year == date.today().year + 1:
        cf_id = None

    # Condition if the sop date of the tooling is before the first cf
    elif request.date_sop < cf03.date_exp:
        cf_id = cf03.id

    # Condition if the sop date of the tooling is before the second cf
    elif request.date_sop < cf05.date_exp:
        cf_id = cf05.id

    # Condition if the sop date of the tooling is before the third cf
    elif request.date_sop < cf07.date_exp:
        cf_id = cf07.id

    else:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Invalid information",
        )

    return bp_id, cf_id


def set_client_description(request: toolingSchema, db: Session):
    client = db.query(Client).filter_by(name=request.client.name).first()

    if not client:
        client = Client(
            name=request.client.name,
        )
        db.add(client)
        db.commit()
        db.refresh(client)

    return client


@router.get("", response_model=Page[toolingResponseSchema])
async def get_all(
    db: Session = Depends(get_db), user=Depends(get_current_user_azure)
) -> Page[toolingResponseSchema]:
    if user.get("roles")[0] == "PPS":
        return paginate(db, select(Tooling).order_by(Tooling.id))

    request_type = (
        db.query(RequestType).filter(RequestType.desc == user.get("roles")[0]).first()
    )
    return paginate(
        db,
        select(Tooling)
        .filter(
            and_(
                Tooling.request_type == request_type.id,
                Tooling.requested_by == user["preferred_username"],
            )
        )
        .order_by(Tooling.id),
    )


@router.get("/{id}", response_model=toolingWithHistoric)
def get_by_id(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user_azure)
):
    if user.get("roles")[0] == "PPS":
        tooling = db.query(Tooling).filter(Tooling.id == id).first()
        return tooling

    request_type = (
        db.query(RequestType).filter(RequestType.desc == user.get("roles")[0]).first()
    )
    search_tooling = db.query(Tooling).filter(Tooling.id == id).first()

    if not search_tooling:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tooling não encontrado"
            )
        )

    if (
        search_tooling.request_type == request_type.id
        and search_tooling.requested_by == user["preferred_username"]
    ):
        return search_tooling
    else:
        raise (
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não está autorizado a ver essa informação",
            )
        )


@router.post("", response_model=toolingResponseSchema)
def add(
    request: toolingSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if user.get("roles")[0] == "PPS":
        raise (
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não está autorizado a fazer essa requisição",
            )
        )

    tooling_type = db.query(ToolingType).filter_by(desc=request.tooling_t.desc).first()
    product_type = db.query(ProductType).filter_by(desc=request.product.desc).first()
    request_type = db.query(RequestType).filter_by(desc=user.get("roles")[0]).first()

    bp, cf = set_status_description(request, db)
    client = set_client_description(request, db)

    new_tooling = Tooling(
        project=request.project,
        client_supplier=client.id,
        part_number=request.part_number,
        price=request.price,
        request_type=request_type.id,
        product_type=product_type.id,
        tooling_type=tooling_type.id,
        requested_by=user["preferred_username"],
        date_input=date.today(),
        date_request=request.date_request,
        date_sop=request.date_sop,
        RBSNO=request.RBSNO,
        bp_id=bp,
        cf_id=cf,
    )

    db.add(new_tooling)
    db.commit()
    db.refresh(new_tooling)

    return new_tooling


@router.put("/{id}")
def update(
    id: int,
    request: toolingSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    query = db.query(Tooling).filter(Tooling.id == id)
    tooling: Tooling = query.first()

    if not tooling:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tooling não encontrado"
            )
        )

    if not tooling.requested_by == user["preferred_username"]:
        raise (
            HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não está autorizado a fazer essa requisição",
            )
        )

    # Verifying if the tooling is able to be modified
    if tooling.was_approved == True:

        today = date.today()
        bp_date = db.query(DateBP).filter_by(id=tooling.bp.id).first()
        cf_date = db.query(DateCF).filter_by(id=tooling.cf_id).first()

        exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é possível alterar esse tooling",
        )

        if bp_date.date_exp < today:
            raise exception

        if tooling.cf_id and cf_date.date_exp < today:
            raise exception

    tooling_type = db.query(ToolingType).filter_by(desc=request.tooling_t.desc).first()
    product_type = db.query(ProductType).filter_by(desc=request.product.desc).first()
    request_type = db.query(RequestType).filter_by(desc=user.get("roles")[0]).first()

    bp, cf = set_status_description(request, db)
    client = set_client_description(request, db)

    print(tooling_type)
    print(dir(tooling_type))

    tooling_updated = ToolingUpdates(
        tooling_fk=tooling.id,
        project=tooling.project,
        client_supplier=client.id,
        part_number=tooling.part_number,
        price=tooling.price,
        request_type=request_type.id,
        product_type=product_type.id,
        tooling_type=tooling_type.id,
        date_input=tooling.date_input,
        date_request=tooling.date_request,
        date_sop=tooling.date_sop,
        RBSNO=tooling.RBSNO,
    )

    db.add(tooling_updated)

    dicionario = request.model_dump()
    dicionario.pop("client")
    dicionario.pop("product")
    dicionario.pop("tooling_t")
    dicionario["client_supplier"] = client.id
    dicionario["request_type"] = request_type.id
    dicionario["product_type"] = product_type.id
    dicionario["tooling_type"] = tooling_type.id
    dicionario["cf_id"] = cf
    dicionario["bp"] = bp
    query.update(dicionario)
    db.commit()
    return dicionario


@router.post("/{id}/part-number")
def update_part_number(
    id: int,
    request: partNumberSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if not user.get("roles")[0] == "SO":
        raise (
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não está autorizado a fazer essa requisição",
            )
        )

    tooling = db.query(Tooling).filter(Tooling.id == id).first()

    if not tooling:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tooling não encontrado"
            )
        )

    tooling.part_number = request.part_number
    db.commit()
    return request


@router.post("/{id}/status")
def update_status(
    id: int,
    request: statusSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_azure),
):
    if not user.get("roles")[0] == "PPS":
        raise (
            HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não está autorizado a fazer essa requisição",
            )
        )

    tooling = db.query(Tooling).filter(Tooling.id == id).first()

    if not tooling:
        pass

    tooling.was_approved = request.status
    if request.status == False:
        tooling.status_description = request.status_description
    db.commit()
    db.refresh(tooling)
    return tooling


# @router.delete("/{id}")
# def delete(
#     id: int, db: Session = Depends(get_db), user=Depends(get_current_user_azure)
# ):
#     deleted_type = db.query(Tooling).filter(Tooling.id == id).first()
#     if deleted_type:
#         db.delete(deleted_type)
#         db.commit()
#         return {"Type deleted"}
#     return {"Not Founded"}

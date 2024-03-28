""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, and_, or_

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

    today = date.today()
    request.date_sop = date(2024, 11, 1)

    # Getting the BP of the sop year
    bp = db.query(DateBP).filter(DateBP.desc == f"{request.date_sop.year}"[2:]).first()

    if not bp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid BP",
        )

    # In case, input date before BP expiration date
    if today <= bp.date_exp:
        return bp.id, None

    # Getting all the related CFs
    cf_list = db.query(DateCF).filter(DateCF.bp == bp.id).all()

    if not cf_list or len(cf_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CFs for this BP",
        )

    for cf in cf_list:
        if today < cf.date_exp:
            return bp.id, cf.id

    raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        detail="You cannot request a tooling, for this year after all CFs close",
    )


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


def set_query(bp_search: str, cf_search: str, user, db: Session):

    # Setting variables
    preferred_username = user.get("preferred_username")
    role = user.get("roles")[0]

    exception_not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    bp = None
    cf = None

    # In case a BP is searched
    if bp_search:
        bp = db.query(DateBP).filter(DateBP.desc == bp_search).first()
        if not bp:
            raise exception_not_found

        # In case a CF is searched
        if cf_search:
            cf = db.query(DateCF).filter(DateCF.desc == cf_search).first()
            if not bp:
                raise exception_not_found

    # In case of user role is PPS, it must show all toolings
    if role == "PPS":

        # Searching by BP and CF:
        if bp and cf:
            return select(Tooling).filter(
                and_(
                    Tooling.bp_id == bp.id,
                    Tooling.cf_id == cf.id,
                )
            )

        # Searching by only BP
        elif bp:
            return select(Tooling).filter(
                and_(
                    Tooling.bp_id == bp.id,
                )
            )

        # In case neither BP or CF was searched, getting all
        return select(Tooling)

    # In case of user role is not PPS, searching only for
    else:

        # Verifying if user is from ICT or RPP
        request_type = db.query(RequestType).filter(RequestType.desc == role).first()

        # Searching by BP and CF:
        if bp and cf:
            return select(Tooling).filter(
                and_(
                    Tooling.bp_id == bp.id,
                    Tooling.cf_id == cf.id,
                    Tooling.request_type == request_type.id,
                    Tooling.requested_by == preferred_username,
                )
            )

        # Searching by only BP
        elif bp:
            return select(Tooling).filter(
                and_(
                    Tooling.bp_id == bp.id,
                    Tooling.request_type == request_type.id,
                    Tooling.requested_by == preferred_username,
                )
            )

        # In case neither BP or CF was searched, getting all
        return select(Tooling)


@router.get("", response_model=Page[toolingResponseSchema])
async def get_all(
    db: Session = Depends(get_db),
    tooling_search: str = "",
    bp_search: str = "",
    cf_search: str = "",
    user=Depends(get_current_user_azure),
) -> Page[toolingResponseSchema]:

    # # Dummy User for tests:
    # user = {"roles": ["PPS"], "preferred_username": "ct67ca@bosch.com"}
    return paginate(
        db,
        set_query(
            db=db,
            bp_search=bp_search,
            cf_search=cf_search,
            user=user,
        )
        .filter(
            or_(
                Tooling.project.contains(tooling_search),
                Tooling.part_number.contains(tooling_search),
                Tooling.requested_by.contains(tooling_search),
            )
        )
        .order_by(-Tooling.id),
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
                status_code=status.HTTP_404_NOT_FOUND, detail="Tooling not founded"
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
                detail="You are not authorized to this information",
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
                detail="You are not authorized to this information",
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
                status_code=status.HTTP_404_NOT_FOUND, detail="Tooling not founded"
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
            detail="Is not possible update this tooling",
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
    dicionario["bp_id"] = bp
    query.update(dicionario)
    db.commit()
    return dicionario


@router.patch("/{id}/part-number")
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
                detail="You are not authorized to this request",
            )
        )

    tooling = db.query(Tooling).filter(Tooling.id == id).first()

    if not tooling:
        raise (
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tooling not found"
            )
        )

    tooling.part_number = request.part_number
    db.commit()
    return request


@router.patch("/{id}/status")
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
                detail="You are not authorized to this request",
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

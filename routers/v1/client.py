""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Client
from core.schemas import clientSchema
from core.exceptions import EXCEPTIONS
from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["Client"],
    prefix="/client",
)


@router.get("", response_model=List[clientSchema])
def get_all(db: Session = Depends(get_db), user = Depends(get_current_user_azure)):
    clients = db.query(Client).all()
    return clients


# @router.get("/{id}", response_model=descSchema)
@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise EXCEPTIONS.CLIENT.NOT_FOUND

    return client


@router.post("", response_model=clientSchema)
def add(request: clientSchema, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):

    client = Client(
        name=request.name,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.put("/{id}")
def update(id: int, request: clientSchema, db: Session = Depends(get_db), user = Depends(get_current_user_azure)):

    client = db.query(Client).filter(Client.id == id)
    if not client:
        raise EXCEPTIONS.CLIENT.NOT_FOUND

    if not client:
        pass

    client.update(request.model_dump())
    db.commit()
    return request


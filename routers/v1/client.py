""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends
from typing import List
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Client
from core.schemas import descSchema, descResponseSchema


router = APIRouter(
    tags=["Client"],
    prefix="/client",
)


@router.get("", response_model=List[descResponseSchema])
def get_all(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients


@router.get("/{id}", response_model=descSchema)
def get_by_id(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    return client


@router.post("", response_model=descSchema)
def add(request: descSchema, db: Session = Depends(get_db)):

    client = Client(
        desc=request.desc,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.put("/{id}")
def update(id: int, request: descSchema, db: Session = Depends(get_db)):

    old_type = db.query(Client).filter(Client.id == id)
    if not old_type:
        pass

    old_type.update(request.model_dump())
    db.commit()
    return request


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):

    deleted_type = db.query(Client).filter(Client.id == id).first()
    if deleted_type:
        db.delete(deleted_type)
        db.commit()
        return {"Type deleted"}
    return {"Not Founded"}

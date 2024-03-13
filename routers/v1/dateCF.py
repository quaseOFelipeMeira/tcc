""" File to define endpoints for request Type ( ICT / RRP / TLM / ...)
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import DateCF
from core.schemas import (
    dateCF
)

from datetime import date

from configs.deps import get_current_user_azure

router = APIRouter(
    tags=["DateCF"],
    prefix="/dateCF",
)


@router.post("", response_model=dateCF)
def add(request: dateCF, db: Session = Depends(get_db), user=Depends(get_current_user_azure)):
    # if user.get("roles")[0] != "PPS":
    #     raise(HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Você não está autorizado a fazer essa requisição"))        

    new_dateCF = DateCF(
        desc=request.desc,
        date_exp=request.date_exp
    )
    
    db.add(new_dateCF)
    db.commit()
    db.refresh(new_dateCF)
    return new_dateCF

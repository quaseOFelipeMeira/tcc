from fastapi import APIRouter
from . import requestType, toolingType, productType


router = APIRouter(prefix="/v1")

router.include_router(requestType.router)
router.include_router(toolingType.router)
router.include_router(productType.router)

from fastapi import APIRouter
from . import requestType, toolingType, productType, tooling, client, dateCF


router = APIRouter(prefix="/v1")

router.include_router(tooling.router)
router.include_router(requestType.router)
router.include_router(toolingType.router)
router.include_router(productType.router)
router.include_router(client.router)
router.include_router(dateCF.router)

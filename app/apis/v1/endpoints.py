from fastapi import APIRouter
from .routers.auth import router as auth_router

router = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
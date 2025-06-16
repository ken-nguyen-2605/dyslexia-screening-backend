from fastapi import APIRouter
from .routers.auth import router as auth_router
from .routers.test_session import router as test_session_router

router = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
router.include_router(test_session_router)
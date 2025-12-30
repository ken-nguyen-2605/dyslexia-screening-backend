from fastapi import APIRouter

from .routers.account import router as account_router
from .routers.admin.account import router as admin_account_router
from .routers.auth import router as public_auth_router
from .routers.users import router as user_router
from .routers.user.test_session import router as test_session_router
from .routers.user.minigame import router as minigame_router

router = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
)

# Public routes
router.include_router(public_auth_router)

# Account-required routes (require account authentication, no profile selection needed)
router.include_router(account_router)

# User routes (require account authentication and profile selection)
router.include_router(user_router)
router.include_router(test_session_router)
router.include_router(minigame_router)

# Admin routes
router.include_router(admin_account_router)

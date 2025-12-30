
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.profile import Profile
from app.schemas.account import (
    AccountSchema,
    ProfileCreateRequest,
    ProfileSchema,
    ProfileUpdateRequest,
)
from app.schemas.auth import Token
from app.utils.auth import create_access_token, get_current_account
from app.utils.auth import get_current_profile as get_current_profile_middleware

router = APIRouter(
    prefix="/user",
    tags=["User - profile"],
    responses={404: {"description": "Not found"}},
)

@router.get("/profiles/me", response_model=ProfileSchema)
async def get_current_profile(
    current_profile: Profile = Depends(get_current_profile_middleware),
):
    """ATTENTION: The endpoints below require profile selection."""
    return current_profile
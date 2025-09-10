from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.utils.auth import get_current_profile

from app.models.profile import Profile
from app.schemas.auth import ProfileSchema

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_profile)]
)

@router.get("/profile", response_model=ProfileSchema)
async def get_profile(current_profile: Profile = Depends(get_current_profile)):
    return current_profile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.utils.auth import get_current_profile

from app.models.profile import Profile
from app.schemas.auth import ProfileSchema, ProfileUpdateRequest

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_profile)]
)

@router.get("/profile", response_model=ProfileSchema)
async def get_profile(current_profile: Profile = Depends(get_current_profile)):
    return current_profile

@router.put("/profile", response_model=ProfileSchema)
async def update_profile(updated_profile: ProfileUpdateRequest, db: Session = Depends(get_db), current_profile: Profile = Depends(get_current_profile)):
    """
    Update the current user's profile with the provided data.\n
    Suggest for frontend:\n
    Case 1: User updates in their own profile settings.\n
    Case 2: When taking user details for the first time starting the test.
    """
    for key, value in updated_profile.model_dump(exclude_unset=True).items():
        setattr(current_profile, key, value)
    try:
        db.add(current_profile)
        db.commit()
        db.refresh(current_profile)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile update failed due to integrity error.")
    return current_profile
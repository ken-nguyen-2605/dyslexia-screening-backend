"""These routes require authentication for account only,
no profile selection needed, EXCEPT GET CURRENT PROFILE"""

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
    prefix="/account",
    tags=["Account - account & profile"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=AccountSchema)
async def read_current_account(current_account: Account = Depends(get_current_account)):
    """Get details of the currently authenticated account."""
    return current_account


@router.post("/profiles", response_model=ProfileSchema)
async def create_profile(
    profile_request: ProfileCreateRequest,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    """Create a new profile for the current account."""
    new_profile = Profile(
        profile_type=profile_request.profile_type,
        name=profile_request.name,
        account_id=current_account.id,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/profiles", response_model=list[ProfileSchema])
async def get_profiles(current_account: Account = Depends(get_current_account)):
    """Get all profiles associated with the current account."""
    return current_account.profiles

@router.get("/profiles/{profile_id}", response_model=ProfileSchema)
async def get_profile(
    profile_id: int, current_account: Account = Depends(get_current_account)
):
    """Get a specific profile by ID for the current account."""
    profile = next((p for p in current_account.profiles if p.id == profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/profiles/{profile_id}", response_model=ProfileSchema)
async def update_profile(
    profile_id: int,
    updated_profile: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_account: Profile = Depends(get_current_account),
):
    """
    Update the current user's profile with the provided data.\n
    Suggest for frontend:\n
    Case 1: User updates in their own profile settings.\n
    Case 2: When taking user details for the first time starting the test.
    """
    profile = next((p for p in current_account.profiles if p.id == profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in updated_profile.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    try:
        db.add(profile)
        db.commit()
        db.refresh(profile)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile update failed due to integrity error.",
        )

    return profile


@router.delete("/profiles/{profile_id}", status_code=204)
async def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    profile = next((p for p in current_account.profiles if p.id == profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()


@router.post("/profiles/{profile_id}/select", response_model=Token)
async def select_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    profile = next((p for p in current_account.profiles if p.id == profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    access_token = create_access_token(
        data={"account_id": str(current_account.id), "profile_id": str(profile.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

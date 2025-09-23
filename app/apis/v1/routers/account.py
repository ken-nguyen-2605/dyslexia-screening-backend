from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import create_access_token, get_current_account

from app.models.account import Account
from app.models.profile import Profile
from app.schemas.auth import Token
from app.schemas.auth import ProfileSchema
from app.schemas.account import ProfileCreateRequest

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}}
)

@router.post("/profiles", response_model=ProfileSchema)
async def create_profile(profile_request: ProfileCreateRequest, db: Session = Depends(get_db), current_account: Account = Depends(get_current_account)):
    new_profile = Profile(
        profile_type=profile_request.profile_type,
        name=profile_request.name,
        account_id=current_account.id
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/profiles", response_model=list[ProfileSchema])
async def get_profiles(current_account: Account = Depends(get_current_account)):
    print("Current account profiles:", current_account.profiles)
    return current_account.profiles

@router.delete("/profiles/{profile_id}", status_code=204)
async def delete_profile(profile_id: int, db: Session = Depends(get_db), current_account: Account = Depends(get_current_account)):
    profile = next((p for p in current_account.profiles if p.id == profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    
@router.post("/profiles/{profile_id}/select", response_model=Token)
async def select_profile(profile_id: int, db: Session = Depends(get_db), current_account: Account = Depends(get_current_account)):
    profile = next((p for p in current_account.profiles if p.id == profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    access_token = create_access_token(data={"account_id": str(current_account.id), "profile_id": str(profile.id)})
    return {"access_token": access_token, "token_type": "bearer"}
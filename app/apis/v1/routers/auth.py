from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import hash_password, verify_password, create_access_token

from app.models.account import Account
from app.models.profile import Profile
from app.models.enums import ProfileType

from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)        

@router.post("/register")
async def register(register_request: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    existing = db.query(Account).filter(Account.email == register_request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    profile = Profile(
        profile_type=ProfileType.PARENT,
        name=register_request.profile_name,
    )
    
    account = Account(
        email=register_request.email,
        hashed_password=hash_password(register_request.password),
        profiles=[profile]
    )
    
    db.add(account)
    db.commit()
    db.refresh(account)

    return RegisterResponse(
        id=account.id,
        email=account.email,
        profile_name=profile.name,
        created_at=account.created_at
    )

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.email == login_request.email).first()

    if not account or not verify_password(login_request.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
            
    access_token = create_access_token(data={"account_id": str(account.id)})
    return {"access_token": access_token, "token_type": "bearer"}
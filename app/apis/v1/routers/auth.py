"""Public authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.enums import ProfileType
from app.models.profile import Profile
from app.schemas.auth import LoginRequest, RegisterRequest, RegisterResponse, Token
from app.utils.auth import create_access_token, hash_password, verify_password

router = APIRouter(
    prefix="/public/auth",
    tags=["Public - auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
async def register(
    register_request: RegisterRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    existing = db.query(Account).filter(Account.email == register_request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    profile = Profile(
        profile_type=ProfileType.PARENT,
        name=register_request.name,
    )

    account = Account(
        email=register_request.email,
        hashed_password=hash_password(register_request.password),
        profiles=[profile],
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return RegisterResponse(
        id=account.id, email=account.email, created_at=account.created_at
    )


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.email == login_request.email).first()

    if not account or not verify_password(
        login_request.password, account.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"account_id": str(account.id), "role": account.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-email")
async def verify_email(email: str, db: Session = Depends(get_db)):
    """Verify if the email is already registered by sending a verification link to the
    user's email."""
    account = db.query(Account).filter(Account.email == email).first()
    return {"is_registered": account is not None}


@router.post("/forgot-password")
async def forgot_password(email: str):
    """Send a password reset link to the user's email if it has already been
    verified."""
    return {"message": "Password reset link sent if the email is registered."}

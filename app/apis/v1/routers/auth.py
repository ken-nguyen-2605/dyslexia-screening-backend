from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import hash_password, verify_password, create_access_token

from app.models.account import Account
from app.models.profile import Profile
from app.models.enums import ProfileType

from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse

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

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.email == login_request.email).first()

    if not account or not verify_password(login_request.password, account.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
            
    access_token = create_access_token(data={"sub": str(account.id)})
    return LoginResponse(
        id=account.id,
        access_token=access_token,
        profiles=[
            Profile(
                id=profile.id,
                profile_type=profile.profile_type,
                name=profile.name,
                created_at=profile.created_at
            ) for profile in account.profiles
        ],
        token_type="bearer"
    )
    
# @router.post("/guest", response_model=GuestResponse)
# async def guest(guest_request: GuestRequest, db: Session = Depends(get_db)):
#     guest = db.query(Participant).filter(Participant.email == guest_request.email).first()
#     if guest and guest.participant_type != ParticipantType.GUEST:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered as a user"
#         )
    
#     if not guest:
#         guest_part = GuestParticipant(participant=guest)
#         guest = Participant(
#             email=guest_request.email,
#             participant_type=ParticipantType.GUEST,
#             guest_participant=guest_part
#         )
        
#         db.add(guest)
#         db.commit()
#         db.refresh(guest)
        
#     access_token = create_access_token(data={"sub": str(guest.id)})
#     return GuestResponse(
#         id=guest.id,
#         email=guest.email,
#         access_token=access_token,
#         created_at=guest.created_at
#     )
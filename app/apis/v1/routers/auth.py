from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import hash_password, verify_password, create_access_token

from app.models.participant import Participant
from app.models.user_participant import UserParticipant
from app.models.guest_participant import GuestParticipant
from app.models.enums import ParticipantType
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, GuestRequest, GuestResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)        

@router.post("/register")
async def register(register_request: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    existing = db.query(Participant).filter(Participant.email == register_request.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    
    participant = Participant(
        email=register_request.email,
        participant_type=ParticipantType.USER
    )
    
    user_part = UserParticipant(
        name=register_request.name,
        hashed_password=hash_password(register_request.password),
        participant=participant
    )
    
    db.add(participant)
    db.commit()
    db.refresh(participant)

    return RegisterResponse(
        id=participant.id,
        name=user_part.name,
        email=participant.email,
        created_at=participant.created_at
    )

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user_participant = db.query(Participant).filter(
        Participant.email == login_request.email,
        Participant.participant_type == ParticipantType.USER
    ).first()
    
    if not user_participant or not verify_password(login_request.password, user_participant.user_participant.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
            
    access_token = create_access_token(data={"sub": str(user_participant.id)})
    return LoginResponse(
        id=user_participant.id,
        access_token=access_token
    )
    
@router.post("/guest", response_model=GuestResponse)
async def guest(guest_request: GuestRequest, db: Session = Depends(get_db)):
    guest = db.query(Participant).filter(Participant.email == guest_request.email).first()
    if guest and guest.participant_type != ParticipantType.GUEST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered as a user"
        )
    
    if not guest:
        guest_part = GuestParticipant(participant=guest)
        guest = Participant(
            email=guest_request.email,
            participant_type=ParticipantType.GUEST,
            guest_participant=guest_part
        )
        
        db.add(guest)
        db.commit()
        db.refresh(guest)
        
    access_token = create_access_token(data={"sub": str(guest.id)})
    return GuestResponse(
        id=guest.id,
        email=guest.email,
        access_token=access_token,
        created_at=guest.created_at
    )
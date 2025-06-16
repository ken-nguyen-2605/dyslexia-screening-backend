from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.participant import UserParticipantOut, GuestParticipantOut
from app.models.participant import Participant

import jwt
import bcrypt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from app.models.enums import ParticipantTypeEnum

# Security configurations
bearer_security = HTTPBearer(auto_error=False)

# Hashing passwords
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT token
def create_access_token(data: dict[str]) -> str:
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({
        "exp": expire_time,
        "iat": datetime.now(timezone.utc),
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_participant(request: Request, auth_header: HTTPAuthorizationCredentials = Depends(bearer_security), db: Session = Depends(get_db)) -> UserParticipantOut | GuestParticipantOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if auth_header is None or not auth_header.credentials:
        raise credentials_exception
    
    token = auth_header.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        participant_id: int = payload.get("sub")
        if participant_id is None:
            raise credentials_exception
        participant_id = int(participant_id)       
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    except InvalidTokenError:
        print("Token is invalid")
        print(f"Token: {token}")
        raise credentials_exception
    
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    
    if participant.participant_type == ParticipantTypeEnum.GUEST:
        guest = participant.guest_participant        
        return GuestParticipantOut(
            id=participant.id,
            participant_type=participant.participant_type,
            email=participant.email,
            created_at=participant.created_at,
            last_activity=guest.last_activity
        )
        
    elif participant.participant_type == ParticipantTypeEnum.USER:
        user = participant.user_participant
        return UserParticipantOut(
            id=participant.id,
            participant_type=participant.participant_type,
            email=participant.email,
            created_at=participant.created_at,
            name=user.name,
            last_login=user.last_login
        )
        
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown participant type")
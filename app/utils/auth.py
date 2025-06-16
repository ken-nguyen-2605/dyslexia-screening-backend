from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.background import BackgroundTasks

from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.participant import ParticipantOut
from app.models.participant import Participant
from app.models.guest_participant import GuestParticipant
from app.models.user_participant import UserParticipant

import jwt
import bcrypt
from jwt.exceptions import InvalidTokenError

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
def create_access_token(data: dict[str], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire_time = datetime.now(timezone.utc) + expires_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({
        "exp": expire_time,
        "iat": datetime.now(timezone.utc),
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
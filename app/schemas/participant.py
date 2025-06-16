from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime
from app.models.enums import ParticipantTypeEnum

class ParticipantBase(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the participant")]
    participant_type: Annotated[ParticipantTypeEnum, Field(..., description="Type of the participant (USER or GUEST)")]
    email: Annotated[EmailStr, Field(..., description="Email address of the participant")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the participant was created")]
    
    model_config = {
        "from_attributes": True,
    }

class UserParticipantOut(ParticipantBase):
    name: Annotated[str, Field(..., max_length=128, description="Name of the user participant")]
    last_login: Annotated[Optional[datetime], Field(None, description="Timestamp of the last login of the user participant")]

class GuestParticipantOut(ParticipantBase):
    last_activity: Annotated[Optional[datetime], Field(None, description="Timestamp of the last activity of the guest participant")]
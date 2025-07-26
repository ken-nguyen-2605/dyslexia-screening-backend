from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime

# PROFILE SCHEMAS
class ProfileResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    name: Annotated[str, Field(..., max_length=128, description="Name of the user")]
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the user was created")]
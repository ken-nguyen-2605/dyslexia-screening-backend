from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime
from ..models.enums import ProfileType

# ACCOUNT SCHEMAS
class AccountSchema(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the account")]
    email: Annotated[EmailStr, Field(..., max_length=255, description="Email address of the account")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the account was created")]
    
    model_config = {
        "from_attributes": True
    }
    
class AccountUpdateRequest(BaseModel):
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="New password for the account")]
    
# PROFILE SCHEMAS
class ProfileSchema(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the profile")]
    profile_type: Annotated[ProfileType, Field(..., description="Type of the profile")]
    name: Annotated[str, Field(..., max_length=50, description="Display name of the profile")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the profile was created")]
    
    model_config = {
        "from_attributes": True
    }
    
class ProfileSelectRequest(BaseModel):
    account_id: Annotated[int, Field(..., description="Unique identifier of the account")]
    profile_id: Annotated[int, Field(..., description="Unique identifier of the profile to select")]
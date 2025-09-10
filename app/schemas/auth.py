from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime
from ..models.enums import ProfileType

# TOKEN SCHEMAS
class Token(BaseModel):
    access_token: Annotated[str, Field(..., description="JWT access token")]
    token_type: Annotated[str, Field(default="bearer", description="Type of the token, usually 'bearer'")]
    
# PROFILE SCHEMAS
class Profile(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the profile")]
    profile_type: Annotated[ProfileType, Field(..., description="Type of the profile")]
    name: Annotated[str, Field(..., max_length=50, description="Display name of the profile")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the profile was created")]
    
# REGISTER SCHEMAS
class RegisterRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for the user")]
    profile_name: Annotated[str, Field(..., max_length=50, description="Display name of the default profile")]

class RegisterResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    profile_name: Annotated[str, Field(..., max_length=50, description="Display name of the default profile")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the user was created")]

# LOGIN SCHEMAS
class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for the user")]
    
class LoginResponse(Token):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    profiles: Annotated[list[Profile], Field(..., description="List of profiles associated with the user")]
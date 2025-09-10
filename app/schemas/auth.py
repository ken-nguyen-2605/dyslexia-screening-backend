from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime
from ..models.enums import ProfileType, Gender

# TOKEN SCHEMAS
class Token(BaseModel):
    access_token: Annotated[str, Field(..., description="JWT access token")]
    token_type: Annotated[str, Field(default="bearer", description="Type of the token, usually 'bearer'")]
    
# PROFILE SCHEMAS
class ProfileSchema(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the profile")]
    profile_type: Annotated[ProfileType, Field(..., description="Type of the profile")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the profile was created")]
    
    # Info about user when they enter the test
    name: Annotated[str | None, Field(None, max_length=100, description="Name of the user")] = None
    year_of_birth: Annotated[int | None, Field(None, ge=1900, le=datetime.now().year, description="Year of birth of the user")] = None
    gender: Annotated[Gender | None, Field(None, description="Gender of the user")] = None
    hobbies: Annotated[str | None, Field(None, max_length=255, description="Hobbies of the user")] = None
    
    model_config = {
        "from_attributes": True
    }
    
class ProfileUpdateRequest(BaseModel):
    name: Annotated[str, Field(..., max_length=100, description="Name of the user")]
    year_of_birth: Annotated[int, Field(..., ge=1900, le=datetime.now().year, description="Year of birth of the user")]
    gender: Annotated[Gender, Field(..., description="Gender of the user")]
    hobbies: Annotated[str, Field(..., max_length=255, description="Hobbies of the user")]
    
# REGISTER SCHEMAS
class RegisterRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for the user")]

class RegisterResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the user was created")]

# LOGIN SCHEMAS
class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for the user")]
    
class LoginResponse(Token):
    pass
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime

# TOKEN SCHEMAS
class Token(BaseModel):
    access_token: Annotated[str, Field(..., description="JWT access token")]
    token_type: Annotated[str, Field(default="bearer", description="Type of the token, usually 'bearer'")]
    
# REGISTER SCHEMAS
class RegisterRequest(BaseModel):
    name: Annotated[str, Field(..., max_length=128, description="Name of the user")]
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for the user")]

class RegisterResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    name: Annotated[str, Field(..., max_length=128, description="Name of the user")]
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the user was created")]

    model_config = {
        "orm_mode": True
    }

# LOGIN SCHEMAS
class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(..., max_length=128, description="Email address of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128, description="Password for the user")]
    
class LoginResponse(Token):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    
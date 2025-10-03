from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from ..models.enums import AccountRole

"""
1. TOKEN SCHEMAS
2. REGISTER SCHEMAS
3. LOGIN SCHEMAS
"""


# TOKEN SCHEMAS
class Token(BaseModel):
    access_token: Annotated[str, Field(..., description="JWT access token")]
    token_type: Annotated[
        str, Field(default="bearer", description="Type of the token, usually 'bearer'")
    ]


# REGISTER SCHEMAS
class RegisterRequest(BaseModel):
    email: Annotated[
        EmailStr, Field(..., max_length=128, description="Email address of the user")
    ]
    password: Annotated[
        str,
        Field(..., min_length=8, max_length=128, description="Password for the user"),
    ]


class RegisterResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    email: Annotated[
        EmailStr, Field(..., max_length=128, description="Email address of the user")
    ]
    role: Annotated[
        AccountRole,
        Field(default=AccountRole.USER, description="Role of the user in the system"),
    ] = AccountRole.USER
    created_at: Annotated[
        datetime, Field(..., description="Timestamp when the user was created")
    ]


# LOGIN SCHEMAS
class LoginRequest(BaseModel):
    email: Annotated[
        EmailStr, Field(..., max_length=128, description="Email address of the user")
    ]
    password: Annotated[
        str,
        Field(..., min_length=8, max_length=128, description="Password for the user"),
    ]


class LoginResponse(Token):
    pass

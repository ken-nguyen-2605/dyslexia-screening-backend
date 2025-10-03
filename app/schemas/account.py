from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..models.enums import AccountRole, Gender, OfficialDyslexiaDiagnosis, ProfileType

"""
USER:
1. ACCOUNT SCHEMAS
2. PROFILE SCHEMAS

ADMIN:
3. ACCOUNT ROLE SCHEMAS
4. ACCOUNT CREATE SCHEMAS
"""


# USER - ACCOUNT SCHEMAS
class AccountSchema(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the account")]
    email: Annotated[
        EmailStr, Field(..., max_length=255, description="Email address of the account")
    ]
    created_at: Annotated[
        datetime, Field(..., description="Timestamp when the account was created")
    ]
    role: Annotated[AccountRole, Field(..., description="Role of the account")]
    profiles: Annotated[
        list["ProfileSchema"],
        Field(..., description="List of profiles associated with the account"),
    ]

    model_config = {"from_attributes": True}


# PROFILE SCHEMAS
class ProfileSchema(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the profile")]
    account_id: Annotated[
        int, Field(..., description="Unique identifier of the associated account")
    ]
    profile_type: Annotated[ProfileType, Field(..., description="Type of the profile")]
    created_at: Annotated[
        datetime, Field(..., description="Timestamp when the profile was created")
    ]

    # Optionsal user info fields
    name: Annotated[
        str | None, Field(..., max_length=50, description="Display name of the profile")
    ]
    year_of_birth: Annotated[
        int | None, Field(..., description="Year of birth of the profile user")
    ]
    email: Annotated[
        EmailStr | None, Field(..., description="Email of the profile user")
    ]
    mother_tongue: Annotated[
        str | None, Field(..., description="Mother tongue of the profile user")
    ]
    gender: Annotated[
        Gender | None, Field(..., description="Gender of the profile user")
    ]
    official_dyslexia_diagnosis: Annotated[
        OfficialDyslexiaDiagnosis | None,
        Field(..., description="Official dyslexia diagnosis status"),
    ]

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdateRequest(BaseModel):
    name: Annotated[str, Field(..., max_length=100, description="Name of the user")]
    year_of_birth: Annotated[
        int,
        Field(
            ...,
            ge=1900,
            le=datetime.now().year,
            description="Year of birth of the user",
        ),
    ]
    email: Annotated[
        EmailStr, Field(..., max_length=255, description="Email address of the user")
    ]
    gender: Annotated[Gender, Field(..., description="Gender of the user")]
    mother_tongue: Annotated[
        str, Field(..., max_length=100, description="Mother tongue of the user")
    ]
    official_dyslexia_diagnosis: Annotated[
        OfficialDyslexiaDiagnosis,
        Field(..., description="Official dyslexia diagnosis status of the user"),
    ]


class ProfileCreateRequest(BaseModel):
    profile_type: Annotated[
        ProfileType, Field(..., description="Type of the profile to create")
    ]
    name: Annotated[
        str, Field(..., max_length=50, description="Display name of the profile")
    ]


class ProfileSelectRequest(BaseModel):
    profile_id: Annotated[
        int, Field(..., description="Unique identifier of the profile to select")
    ]


# ADMIN - ACCOUNT ROLE SCHEMAS
class AccountRoleSchema(BaseModel):
    role: Annotated[
        AccountRole,
        Field(..., description="Role of the account, e.g., USER or ADMIN"),
    ]


# ADMIN - ACCOUNT CREATE SCHEMAS
class AccountCreateRequest(BaseModel):
    email: Annotated[
        EmailStr,
        Field(..., max_length=255, description="Email address for the new account"),
    ]
    role: Annotated[
        AccountRole,
        Field(..., description="Role of the account, defaults to USER if not provided"),
    ]

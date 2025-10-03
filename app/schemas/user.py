from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from ..models.enums import Gender, OfficialDyslexiaDiagnosis, ProfileType


# PROFILE SCHEMAS
class ProfileResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier of the user")]
    account_id: Annotated[int, Field(..., description="Account ID of the user")]
    profile_type: Annotated[
        ProfileType, Field(..., max_length=128, description="Email address of the user")
    ]
    created_at: Annotated[
        datetime, Field(..., description="Timestamp when the user was created")
    ]

    name: Annotated[
        str | None, Field(..., max_length=100, description="Name of the user")
    ]
    year_of_birth: Annotated[
        int | None,
        Field(
            ...,
            ge=1900,
            le=datetime.now().year,
            description="Year of birth of the user",
        ),
    ]
    email: Annotated[
        EmailStr | None,
        Field(..., max_length=255, description="Email address of the user"),
    ]
    gender: Annotated[Gender | None, Field(..., description="Gender of the user")]
    mother_tongue: Annotated[
        str | None, Field(..., max_length=100, description="Mother tongue of the user")
    ]
    official_dyslexia_diagnosis: Annotated[
        OfficialDyslexiaDiagnosis | None,
        Field(..., description="Official dyslexia diagnosis status of the user"),
    ]

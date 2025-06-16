from pydantic import BaseModel, Field
from typing import Annotated
from app.models.enums import TestStatus
from datetime import datetime

# TEST START SCHEMA
class TestStartRequest(BaseModel):
    pass

class TestStartResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the test")]
    participant_id: Annotated[int, Field(..., description="ID of the participant who started the test")]
    start_time: Annotated[datetime, Field(..., description="Start time of the test in ISO 8601 format")]
    completion_status: Annotated[TestStatus, Field(..., description="Status of the test completion")]

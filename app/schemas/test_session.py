from pydantic import BaseModel, Field
from typing import Annotated
from app.models.enums import TestStatus
from datetime import datetime

# TEST START SCHEMA
class TestStartRequest(BaseModel):
    pass

class TestStartResponse(BaseModel):
    test_id: Annotated[str, Field(..., description="Unique identifier for the test")]
    start_time: Annotated[datetime, Field(..., description="Start time of the test in ISO 8601 format")]
    completion_status: Annotated[TestStatus, Field(..., description="Status of the test completion")]

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import PredictDyslexia, TestResult, TestStatus, TestType
from app.models.minigame.minigame import MinigameNumber

class MinigameBase(BaseModel):
    minigame_number: Annotated[MinigameNumber, Field(description="The number of the minigame.")]
    score: Annotated[float, Field(description="The score achieved in the minigame, out of 5.")]
    minigame_details: Annotated[dict, Field(description="Detailed information about the minigame attempt.")]
    attempted_at: Annotated[datetime, Field(description="The timestamp when the minigame was attempted.")]
    
    model_config = ConfigDict(from_attributes=True)

class MinigameCreate(MinigameBase):
    pass

class MinigameResponse(MinigameBase):
    id: Annotated[int, Field(description="The unique identifier of the minigame attempt.")]
    profile_id: Annotated[int, Field(description="The identifier of the profile associated with this minigame attempt.")]
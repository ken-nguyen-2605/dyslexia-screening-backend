from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
from app.models.enums import TestStatus
from datetime import datetime, timedelta
from app.models.enums import (
    AuditoryQuestionType,
    VisualQuestionType,
    LanguageQuestionType,
    QuestionCategory,
)

# TEST START SCHEMA
class TestStartRequest(BaseModel):
    pass

class TestStartResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the test")]
    participant_id: Annotated[int, Field(..., description="ID of the participant who started the test")]
    start_time: Annotated[datetime, Field(..., description="Start time of the test in ISO 8601 format")]
    completion_status: Annotated[TestStatus, Field(..., description="Status of the test completion")]


"""
Example JSON request:
{
    "id": 1,
    "questions": [
        {
            "category": "auditory",
            "type": "FREQ_4_CARDS",
        },
        {
            "category": "visual",
            "type": "SYMBOL_4_CARDS",
        },
        {
            "category": "language",
            "type": "VOWELS",
        }
    ]
}
"""

# TEST PROGRESS SCHEMA        
class TestProgressItem(BaseModel):
    category: Annotated[QuestionCategory, Field(..., description="Category of the question")]
    type: Annotated[AuditoryQuestionType | VisualQuestionType | LanguageQuestionType, Field(..., description="Type of the question")]
    
    @model_validator(mode="before")
    def validate_category_and_type(cls, values):
        category = values.get('category')
        question_type = values.get('type')
        
        if category == QuestionCategory.AUDITORY and not isinstance(question_type, AuditoryQuestionType):
            raise ValueError("Invalid question type for auditory category")
        elif category == QuestionCategory.VISUAL and not isinstance(question_type, VisualQuestionType):
            raise ValueError("Invalid question type for visual category")
        elif category == QuestionCategory.LANGUAGE and not isinstance(question_type, LanguageQuestionType):
            raise ValueError("Invalid question type for language category")
        
        return values
    
class TestProgressRequest(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the test session")]
    questions: Annotated[list[TestProgressItem], Field(..., description="List of questions in the test session")]
    
# AUDITORY SUBMISSION SCHEMA
class AuditorySubmissionRequest(BaseModel):
    question_type: Annotated[AuditoryQuestionType, Field(..., description="Type of the auditory question")]
    start_time: Annotated[datetime, Field(..., description="Start time of the question in ISO 8601 format")]
    end_time: Annotated[datetime, Field(..., description="End time of the question in ISO 8601 format")]
    
    first_click_interval: Annotated[timedelta, Field(..., description="Time interval of the first click")]
    second_click_interval: Annotated[timedelta, Field(..., description="Time interval of the second click")]
    third_click_interval: Annotated[timedelta, Field(..., description="Time interval of the third click")]
    fourth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fourth click")]
    fifth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fifth click")]
    sixth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the sixth click")]
    
    duration_from_round: Annotated[timedelta, Field(..., description="Duration from the start of the round")]
    duration_from_interaction: Annotated[timedelta, Field(..., description="Duration from the interaction start")]
    
    total_clicks: Annotated[int, Field(..., description="Total number of clicks during the question")]
    logic: Annotated[bool, Field(..., description="Whether the logic was followed during the question")]
    instructions_viewed: Annotated[int, Field(..., description="Number of times instructions were viewed")]
    
class AuditorySubmissionResponse(AuditorySubmissionRequest):
    id: Annotated[int, Field(..., description="Unique identifier for the auditory submission")]
    model_config = {
        "from_attributes": True,
    }
    
# VISUAL SUBMISSION SCHEMA
class VisualSubmissionRequest(BaseModel):
    question_type: Annotated[VisualQuestionType, Field(..., description="Type of the visual question")]
    start_time: Annotated[datetime, Field(..., description="Start time of the question in ISO 8601 format")]
    end_time: Annotated[datetime, Field(..., description="End time of the question in ISO 8601 format")]
    
    total_clicks: Annotated[int, Field(..., description="Total number of clicks during the question")]
    
    first_click_interval: Annotated[timedelta, Field(..., description="Time interval of the first click")]
    second_click_interval: Annotated[timedelta, Field(..., description="Time interval of the second click")]
    third_click_interval: Annotated[timedelta, Field(..., description="Time interval of the third click")]
    fourth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fourth click")]
    fifth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fifth click")]
    sixth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the sixth click")]
    
    time_last_click: Annotated[timedelta, Field(..., description="Time since the last click in seconds")]
    
    correct_answers: Annotated[int, Field(..., description="Number of correct answers given during the question")]
    wrong_answers: Annotated[int, Field(..., description="Number of wrong answers given during the question")]
    
class VisualSubmissionResponse(VisualSubmissionRequest):
    id: Annotated[int, Field(..., description="Unique identifier for the visual submission")]
    model_config = {
        "from_attributes": True,
    }
    
# LANGUAGE SUBMISSION SCHEMA
class LanguageSubmissionRequest(BaseModel):
    question_type: Annotated[LanguageQuestionType, Field(..., description="Type of the language question")]
    start_time: Annotated[datetime, Field(..., description="Start time of the question in ISO 8601 format")]
    end_time: Annotated[datetime, Field(..., description="End time of the question in ISO 8601 format")]
    
    clicks: Annotated[int, Field(..., description="Number of clicks during the question")]
    hits: Annotated[int, Field(..., description="Number of hits during the question")]
    misses: Annotated[int, Field(..., description="Number of misses during the question")]
    
class LanguageSubmissionResponse(LanguageSubmissionRequest):
    id: Annotated[int, Field(..., description="Unique identifier for the language submission")]
    model_config = {
        "from_attributes": True,
    }
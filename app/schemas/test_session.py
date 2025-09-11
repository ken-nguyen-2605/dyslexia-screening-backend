from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Annotated
from app.models.enums import TestStatus, TestDifficulty, PredictDyslexia
from datetime import datetime

# TEST START SCHEMA
class TestStartRequest(BaseModel):
    test_difficulty: Annotated[TestDifficulty, Field(..., description="Difficulty level of the test, e.g., 'BASIC', 'ADVANCED'")]

class TestStartResponse(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the test")]
    profile_id: Annotated[int, Field(..., description="ID of the profile taking the test")]
    start_time: Annotated[datetime, Field(..., description="Start time of the test in ISO 8601 format")]
    completion_status: Annotated[TestStatus, Field(..., description="Completion status of the test, e.g., 'COMPLETED', 'IN_PROGRESS'")]
    test_difficulty: Annotated[TestDifficulty, Field(..., description="Difficulty level of the test, e.g., 'BASIC', 'ADVANCED'")]
    
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
# QUESTION SCHEMA
class TestQuestion(BaseModel):
    question_no: Annotated[int, Field(..., description="Question number in the test session")]
    correct: Annotated[bool, Field(..., description="Whether the answer was correct")]

# TEST SUBMISSION SCHEMA
class TestSubmissionRequest(BaseModel):
    questions: Annotated[list[TestQuestion], Field(..., description="List of questions in the test session")]
    
    @field_validator('questions')
    def validate_questions(cls, value):
        # Check if it contains exactly 10 questions
        example_question_nos = set(range(1, 11))
        received_question_nos = {q.question_no for q in value}
        if received_question_nos != example_question_nos:
            raise ValueError("Questions must contain exactly 10 questions with question_no from 1 to 10")
        return value
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "questions": [
                    {"question_no": 1, "correct": True},
                    {"question_no": 2, "correct": False},
                    {"question_no": 3, "correct": True},
                    {"question_no": 4, "correct": True},
                    {"question_no": 5, "correct": False},
                    {"question_no": 6, "correct": True},
                    {"question_no": 7, "correct": False},
                    {"question_no": 8, "correct": True},
                    {"question_no": 9, "correct": True},
                    {"question_no": 10, "correct": False},
                ]
            }
        }
    }
    
class TestSubmissionResponse(BaseModel):
    id: Annotated[int, Field(..., description="ID of the test session")]
    profile_id: Annotated[int, Field(..., description="ID of the profile who took the test")]
    start_time: Annotated[datetime, Field(..., description="Start time of the test session in ISO 8601 format")]
    end_time: Annotated[datetime | None, Field(..., description="End time of the test session in ISO 8601 format")]
    test_difficulty: Annotated[TestDifficulty, Field(..., description="Difficulty level of the test session")]
    completion_status: Annotated[TestStatus, Field(..., description="Completion status of the test session")]
    predict_dyslexia: Annotated[PredictDyslexia | None, Field(..., description="Prediction of dyslexia based on the test results")]
    result: Annotated[int, Field(..., description="Total number of correct answers in the test session")]
    
    model_config = {
        "from_attributes": True,
    }

# # TEST PROGRESS SCHEMA        
# class TestProgressItem(BaseModel):
#     category: Annotated[QuestionCategory, Field(..., description="Category of the question")]
#     type: Annotated[AuditoryQuestionType | VisualQuestionType | LanguageQuestionType, Field(..., description="Type of the question")]
    
#     @model_validator(mode="before")
#     def validate_category_and_type(cls, values):
#         category = values.get('category')
#         question_type = values.get('type')
        
#         if category == QuestionCategory.AUDITORY and not isinstance(question_type, AuditoryQuestionType):
#             raise ValueError("Invalid question type for auditory category")
#         elif category == QuestionCategory.VISUAL and not isinstance(question_type, VisualQuestionType):
#             raise ValueError("Invalid question type for visual category")
#         elif category == QuestionCategory.LANGUAGE and not isinstance(question_type, LanguageQuestionType):
#             raise ValueError("Invalid question type for language category")
        
#         return values
    
# class TestProgressRequest(BaseModel):
#     id: Annotated[int, Field(..., description="Unique identifier for the test session")]
#     questions: Annotated[list[TestProgressItem], Field(..., description="List of questions in the test session")]
    
    
# # RATING SCHEMAS
# class FeatureRating(BaseModel):
#     feature: Annotated[QuestionCategory, Field(..., description="Category of the question")]
#     rating: Annotated[int, Field(..., description="Rating for the feature on a scale of 1 to 5")]
    
#     @field_validator('rating')
#     def validate_rating(cls, value):
#         if not (1 <= value <= 5):
#             raise ValueError("Rating must be between 1 and 5")
#         return value
    
# class FeatureRatingRequest(FeatureRating):
#     pass

# class FeatureRatingResponse(FeatureRating):
#     id: Annotated[int, Field(..., description="Unique identifier for the feature rating")]
#     test_session_id: Annotated[int, Field(..., description="ID of the test session for which the rating was given")]
#     test_session_completion_status: Annotated[TestStatus, Field(..., description="Completion status of the test session")]
#     auditory_progress: Annotated[str, Field(..., description="Progress of the auditory test")]
#     visual_progress: Annotated[str, Field(..., description="Progress of the visual test")]
#     language_progress: Annotated[str, Field(..., description="Progress of the language test")]
    
# # AUDITORY SUBMISSION SCHEMA
# class AuditorySubmissionRequest(BaseModel):
#     question_type: Annotated[AuditoryQuestionType, Field(..., description="Type of the auditory question")]
#     start_time: Annotated[datetime, Field(..., description="Start time of the question in ISO 8601 format")]
#     end_time: Annotated[datetime, Field(..., description="End time of the question in ISO 8601 format")]
    
#     first_click_interval: Annotated[timedelta, Field(..., description="Time interval of the first click")]
#     second_click_interval: Annotated[timedelta, Field(..., description="Time interval of the second click")]
#     third_click_interval: Annotated[timedelta, Field(..., description="Time interval of the third click")]
#     fourth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fourth click")]
#     fifth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fifth click")]
#     sixth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the sixth click")]
    
#     duration_from_round: Annotated[timedelta, Field(..., description="Duration from the start of the round")]
#     duration_from_interaction: Annotated[timedelta, Field(..., description="Duration from the interaction start")]
    
#     total_clicks: Annotated[int, Field(..., description="Total number of clicks during the question")]
#     logic: Annotated[bool, Field(..., description="Whether the logic was followed during the question")]
#     instructions_viewed: Annotated[int, Field(..., description="Number of times instructions were viewed")]
    
# class AuditorySubmissionResponse(AuditorySubmissionRequest):
#     id: Annotated[int, Field(..., description="Unique identifier for the auditory submission")]
#     model_config = {
#         "from_attributes": True,
#     }
    
# # VISUAL SUBMISSION SCHEMA
# class VisualSubmissionRequest(BaseModel):
#     question_type: Annotated[VisualQuestionType, Field(..., description="Type of the visual question")]
#     start_time: Annotated[datetime, Field(..., description="Start time of the question in ISO 8601 format")]
#     end_time: Annotated[datetime, Field(..., description="End time of the question in ISO 8601 format")]
    
#     total_clicks: Annotated[int, Field(..., description="Total number of clicks during the question")]
    
#     first_click_interval: Annotated[timedelta, Field(..., description="Time interval of the first click")]
#     second_click_interval: Annotated[timedelta, Field(..., description="Time interval of the second click")]
#     third_click_interval: Annotated[timedelta, Field(..., description="Time interval of the third click")]
#     fourth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fourth click")]
#     fifth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the fifth click")]
#     sixth_click_interval: Annotated[timedelta, Field(..., description="Time interval of the sixth click")]
    
#     time_last_click: Annotated[timedelta, Field(..., description="Time since the last click in seconds")]
    
#     correct_answers: Annotated[int, Field(..., description="Number of correct answers given during the question")]
#     wrong_answers: Annotated[int, Field(..., description="Number of wrong answers given during the question")]
    
# class VisualSubmissionResponse(VisualSubmissionRequest):
#     id: Annotated[int, Field(..., description="Unique identifier for the visual submission")]
#     model_config = {
#         "from_attributes": True,
#     }
    
# # LANGUAGE SUBMISSION SCHEMA
# class LanguageSubmissionRequest(BaseModel):
#     question_type: Annotated[LanguageQuestionType, Field(..., description="Type of the language question")]
#     start_time: Annotated[datetime, Field(..., description="Start time of the question in ISO 8601 format")]
#     end_time: Annotated[datetime, Field(..., description="End time of the question in ISO 8601 format")]
    
#     clicks: Annotated[int, Field(..., description="Number of clicks during the question")]
#     hits: Annotated[int, Field(..., description="Number of hits during the question")]
#     misses: Annotated[int, Field(..., description="Number of misses during the question")]
    
# class LanguageSubmissionResponse(LanguageSubmissionRequest):
#     id: Annotated[int, Field(..., description="Unique identifier for the language submission")]
#     model_config = {
#         "from_attributes": True,
#     }
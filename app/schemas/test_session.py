from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import PredictDyslexia, TestResult, TestStatus, TestType


# TEST SESSION BASE SCHEMA
class TestSessionSchema(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the test session")]
    profile_id: Annotated[
        int,
        Field(..., description="ID of the profile associated with the test session"),
    ]
    start_time: Annotated[
        datetime,
        Field(..., description="Start time of the test session in ISO 8601 format"),
    ]
    end_time: Annotated[
        datetime | None,
        Field(..., description="End time of the test session in ISO 8601 format"),
    ]
    completed: Annotated[
        bool, Field(..., description="Indicates if the test session is completed")
    ]
    taken_auditory_test: Annotated[
        bool, Field(..., description="Indicates if the auditory test was taken")
    ]
    taken_visual_test: Annotated[
        bool, Field(..., description="Indicates if the visual test was taken")
    ]
    taken_language_test: Annotated[
        bool, Field(..., description="Indicates if the language test was taken")
    ]
    result: Annotated[
        TestResult | None, Field(..., description="Result of the test session")
    ]
    score: Annotated[
        float | None,
        Field(..., description="Overall score of the test session over 100"),
    ]

    model_config = ConfigDict(from_attributes=True)


class SpecificTestSessionCreateSchema(BaseModel):
    test_type: Annotated[
        TestType,
        Field(
            ...,
            description="Type of the test to start, e.g., 'AUDITORY', 'VISUAL', 'LANGUAGE'",
        ),
    ]


class SpecificTestSessionSchema(BaseModel):
    id: Annotated[
        int, Field(..., description="Unique identifier for the auditory test session")
    ]
    test_session_id: Annotated[
        int, Field(..., description="ID of the associated test session")
    ]
    score: Annotated[
        float | None, Field(..., description="Score of the auditory test over 100")
    ]
    test_details: Annotated[
        dict | None,
        Field(..., description="Details of the auditory test in JSON format"),
    ]


class SpecificTestSessionSubmitSchema(SpecificTestSessionSchema):
    test_type: Annotated[
        TestType,
        Field(
            ..., description="Type of the test, e.g., 'AUDITORY', 'VISUAL', 'LANGUAGE'"
        ),
    ]


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

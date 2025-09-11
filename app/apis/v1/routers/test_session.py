from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_profile

from app.models.enums import TestStatus, QuestionType, PredictDyslexia
from app.models.test_session import TestSession

from app.schemas.test_session import (
    TestStartRequest,
    TestStartResponse,
    TestSubmissionRequest,
    TestSubmissionResponse
)

router = APIRouter(
    prefix="/test-session",
    tags=["test-session"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_profile)]
)

QUESTION_MAPPING = {
    1: QuestionType.PHONEMIC_AWARENESS_1,
    2: QuestionType.PHONEMIC_AWARENESS_2,
    3: QuestionType.LETTER_RECOGNITION_1,
    4: QuestionType.LETTER_RECOGNITION_2,
    5: QuestionType.READING_COMPREHENSION_1,
    6: QuestionType.READING_COMPREHENSION_2,
    7: QuestionType.SPELLING_AND_WRITING_1,
    8: QuestionType.SPELLING_AND_WRITING_2,
    9: QuestionType.LANGUAGE_UNDERSTANDING_AND_RECOGNITION_1,
    10: QuestionType.LANGUAGE_UNDERSTANDING_AND_RECOGNITION_2,
}

@router.post("/", response_model=TestStartResponse, status_code=status.HTTP_201_CREATED)
async def start_test(test_start_request: TestStartRequest, db: Session = Depends(get_db), current_profile=Depends(get_current_profile)) -> TestStartResponse:
    """
    Start a new test session for the current participant.
    """
    new_test_session = TestSession(
        profile_id=current_profile.id,
        completion_status=TestStatus.IN_PROGRESS,
        test_difficulty=test_start_request.test_difficulty
    )
    
    db.add(new_test_session)
    db.commit()
    db.refresh(new_test_session)
    
    return TestStartResponse(
        id=new_test_session.id,
        profile_id=new_test_session.profile_id,
        start_time=new_test_session.start_time,
        completion_status=new_test_session.completion_status,
        test_difficulty=new_test_session.test_difficulty
    )
    
@router.get("/", response_model=list[TestSubmissionResponse])
async def get_all_test_sessions_of_user(db: Session = Depends(get_db), current_profile=Depends(get_current_profile)) -> list[TestSubmissionResponse]:
    """
    Retrieve all test sessions for the current profile.
    """
    test_sessions = db.query(TestSession).filter(TestSession.profile_id == current_profile.id).all()
    return [
        TestSubmissionResponse(
            id=ts.id,
            profile_id=ts.profile_id,
            start_time=ts.start_time,
            end_time=ts.end_time,
            completion_status=ts.completion_status,
            test_difficulty=ts.test_difficulty,
            predict_dyslexia=ts.predict_dyslexia,
            result=sum(1 for correct in ts.questions.values() if correct) if ts.questions else 0,
        ) for ts in test_sessions
    ]

@router.post("/{test_session_id}/submit", status_code=status.HTTP_200_OK, response_model=TestSubmissionResponse)
async def submit_test(
    test_session_id: int,
    test_submission_request: TestSubmissionRequest,
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile)
) -> TestSubmissionResponse:
    """
    Submit answers for a specific test session.
    """
    test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.profile_id == current_profile.id).first()
    
    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test session not found."
        )
        
    if test_session.profile_id != current_profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to submit this test session."
        )
        
    if test_session.completion_status != 'IN_PROGRESS':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test session is not in progress."
        )
        
    # Map question_no to correct answer
    questions_dict = {q.question_no: q.correct for q in test_submission_request.questions}
    test_session.questions = questions_dict
    
    result = sum(1 for correct in questions_dict.values() if correct)
    if result >= 7:
        test_session.predict_dyslexia = PredictDyslexia.NO
    elif 4 <= result < 7:
        test_session.predict_dyslexia = PredictDyslexia.MAYBE
    else:
        test_session.predict_dyslexia = PredictDyslexia.YES
    
    # Update test session status to COMPLETED
    test_session.completion_status = TestStatus.COMPLETED
    test_session.end_time = func.now()
    
    db.add(test_session)
    db.commit()
    db.refresh(test_session)
    
    return TestSubmissionResponse(
        id=test_session.id,
        profile_id=test_session.profile_id,
        start_time=test_session.start_time,
        end_time=test_session.end_time,
        completion_status=test_session.completion_status,
        test_difficulty=test_session.test_difficulty,
        predict_dyslexia=test_session.predict_dyslexia,
        result=result,
    )
    
# @router.post("/{test_session_id}/visual", response_model=VisualSubmissionResponse, status_code=status.HTTP_201_CREATED)
# async def submit_visual_features(
#     test_session_id: int,
#     visual_attributes: VisualSubmissionRequest,
#     db: Session = Depends(get_db),
#     current_participant=Depends(get_current_participant)
# ) -> VisualSubmissionResponse:
#     """
#     Submit visual features for a specific test session.
#     """
#     test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.participant_id == current_participant.id).first()
    
#     if not test_session:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Test session not found."
#         )
        
#     if test_session.completion_status != TestStatus.IN_PROGRESS:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Test session is not in progress."
#         )
        
#     if test_session.visual_progress == VisualProgress.COMPLETED:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Visual part of the test is already completed."
#         )
        
#     if visual_attributes.question_type != test_session.visual_progress:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Visual question type does not match the current progress: {test_session.visual_progress}"
#         )
        
#     visual_feature = VisualFeatures(
#         test_session_id=test_session_id,
#         question_type=visual_attributes.question_type,
#         start_time=visual_attributes.start_time,
#         end_time=visual_attributes.end_time,
#         total_clicks=visual_attributes.total_clicks,
#         first_click_interval=visual_attributes.first_click_interval,
#         second_click_interval=visual_attributes.second_click_interval,
#         third_click_interval=visual_attributes.third_click_interval,
#         fourth_click_interval=visual_attributes.fourth_click_interval,
#         fifth_click_interval=visual_attributes.fifth_click_interval,
#         sixth_click_interval=visual_attributes.sixth_click_interval,
#         time_last_click=visual_attributes.time_last_click,
#         correct_answers=visual_attributes.correct_answers,
#         wrong_answers=visual_attributes.wrong_answers
#     )
    
#     test_session.visual_features.append(visual_feature)
#     test_session.visual_progress = list(VisualProgress)[list(VisualProgress).index(visual_attributes.question_type) + 1]
    
#     db.add(visual_feature)
#     try:
#         db.commit()
#     except IntegrityError as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="This type of visual feature has already been submitted for this test session."
#         )
#     db.refresh(visual_feature)
#     db.refresh(test_session)
#     return VisualSubmissionResponse.model_validate(visual_feature)

# @router.post("/{test_session_id}/language", response_model=LanguageSubmissionResponse, status_code=status.HTTP_201_CREATED)
# async def submit_language_features(
#     test_session_id: int,
#     language_attributes: LanguageSubmissionRequest,
#     db: Session = Depends(get_db),
#     current_participant=Depends(get_current_participant)
# ) -> LanguageSubmissionResponse:
#     """
#     Submit language features for a specific test session.
#     """
#     test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.participant_id == current_participant.id).first()
    
#     if not test_session:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Test session not found."
#         )
        
#     if test_session.completion_status != TestStatus.IN_PROGRESS:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Test session is not in progress."
#         )
        
#     if test_session.language_progress == LanguageProgress.COMPLETED:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Language part of the test is already completed."
#         )
        
#     if language_attributes.question_type != test_session.language_progress:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Language question type does not match the current progress: {test_session.language_progress}"
#         )
        
#     language_feature = LanguageFeatures(
#         test_session_id=test_session_id,
#         question_type=language_attributes.question_type,
#         start_time=language_attributes.start_time,
#         end_time=language_attributes.end_time,
#         clicks=language_attributes.clicks,
#         hits=language_attributes.hits,
#         misses=language_attributes.misses
#     )
    
#     test_session.language_features.append(language_feature)
#     test_session.language_progress = list(LanguageProgress)[list(LanguageProgress).index(language_attributes.question_type) + 1]

#     db.add(language_feature)
#     try:
#         db.commit()
#     except IntegrityError as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="This type of language feature has already been submitted for this test session."
#         )
#     db.refresh(language_feature)
#     db.refresh(test_session)
#     return LanguageSubmissionResponse.model_validate(language_feature)

# @router.put("/{test_session_id}/rating", response_model=FeatureRatingResponse, status_code=status.HTTP_200_OK)
# async def feature_rating(
#     test_session_id: int,
#     feature_rating: FeatureRatingRequest,
#     db: Session = Depends(get_db),
#     current_participant=Depends(get_current_participant)
# ) -> FeatureRatingResponse:
#     """
#     Submit a rating for a specific feature in the test session.
#     """
#     test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.participant_id == current_participant.id).first()
#     if not test_session:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Test session not found."
#         )
        
#     if test_session.completion_status != TestStatus.IN_PROGRESS:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Test session is not in progress."
#         )
        
#     match feature_rating.feature:
#         case QuestionCategory.AUDITORY:
#             if test_session.auditory_progress == AuditoryProgress.COMPLETED:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Auditory features have already been rated."
#                 )
#             if test_session.auditory_progress != AuditoryProgress.FEEDBACK:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Auditory features must be submitted before rating."
#                 )
#             test_session.human_feature.auditory_rating = feature_rating.rating
#             test_session.auditory_progress = AuditoryProgress.COMPLETED
            
#         case QuestionCategory.VISUAL:
#             if test_session.visual_progress == VisualProgress.COMPLETED:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Visual features have already been rated."
#                 )
#             if test_session.visual_progress != VisualProgress.FEEDBACK:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Visual features must be submitted before rating."
#                 )
#             test_session.human_feature.visual_rating = feature_rating.rating
#             test_session.visual_progress = VisualProgress.COMPLETED
            
#         case QuestionCategory.LANGUAGE:
#             if test_session.language_progress == LanguageProgress.COMPLETED:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Language features have already been rated."
#                 )
#             if test_session.language_progress != LanguageProgress.FEEDBACK:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Language features must be submitted before rating."
#                 )
#             test_session.human_feature.language_rating = feature_rating.rating
#             test_session.language_progress = LanguageProgress.COMPLETED
            
#         case _:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid feature type."
#             )
        

#     if is_test_completed(test_session):
#         print("Test session is completed")
#         test_session.completion_status = TestStatus.COMPLETED
        
#     db.add(test_session)
#     db.commit()
#     db.refresh(test_session)
    
#     return FeatureRatingResponse(
#         id=test_session.human_feature.id,
#         test_session_id=test_session.id,
#         test_session_completion_status=test_session.completion_status,
#         auditory_progress=test_session.auditory_progress,
#         visual_progress=test_session.visual_progress,
#         language_progress=test_session.language_progress,
#         feature=feature_rating.feature,
#         rating=feature_rating.rating,
#     )
        
# # UTILITIES FUNCTION
# def is_test_completed(test_session: TestSession):
#     """
#     Check if the test session is completed.
#     """
#     return (
#         test_session.auditory_progress == AuditoryProgress.COMPLETED and
#         test_session.visual_progress == VisualProgress.COMPLETED and
#         test_session.language_progress == LanguageProgress.COMPLETED and
#         test_session.human_feature.auditory_rating is not None and
#         test_session.human_feature.visual_rating is not None and
#         test_session.human_feature.language_rating is not None
#     )
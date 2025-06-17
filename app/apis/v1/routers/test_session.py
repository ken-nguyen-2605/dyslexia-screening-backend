from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.utils.auth import get_current_participant
from app.models.test_session import TestSession
from app.models.enums import (
    TestStatus,
    ParticipantType,
    AuditoryQuestionType,
    VisualQuestionType,
    LanguageQuestionType,
    AuditoryProgress,
    VisualProgress,
    LanguageProgress
)
from app.models.auditory_features import AuditoryFeatures
from app.models.visual_features import VisualFeatures
from app.models.language_features import LanguageFeatures
from app.models.human_features import HumanFeatures
from app.schemas.test_session import (
    InfoSubmissionResponse,
    TestStartRequest,
    TestStartResponse,
    AuditorySubmissionRequest,
    AuditorySubmissionResponse,
    VisualSubmissionRequest,
    VisualSubmissionResponse,
    LanguageSubmissionRequest,
    LanguageSubmissionResponse
)

router = APIRouter(
    prefix="/test-session",
    tags=["test-session"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_participant)]
)

@router.post("/", response_model=TestStartResponse, status_code=status.HTTP_201_CREATED)
async def start_test(test_start_request: TestStartRequest, db: Session = Depends(get_db), current_participant=Depends(get_current_participant)):
    """
    Start a new test session for the current participant.
    """
    human_feature = HumanFeatures(
        age=test_start_request.info.age,
        gender=test_start_request.info.gender,
        native_language=test_start_request.info.native_language,
        rl_dyslexia=test_start_request.info.rl_dyslexia,
    )
    new_test_session = TestSession(
        completion_status=TestStatus.IN_PROGRESS,
        participant=current_participant,
        human_feature=human_feature,
        auditory_progress=AuditoryQuestionType.FREQ_4_CARDS,
        visual_progress=VisualQuestionType.SYMBOL_4_CARDS,
        language_progress=LanguageQuestionType.VOWELS,
    )   
    
    db.add(new_test_session)
    db.commit()
    db.refresh(new_test_session)
    
    return TestStartResponse(
        id=new_test_session.id,
        participant_id=new_test_session.participant_id,
        start_time=new_test_session.start_time,
        completion_status=new_test_session.completion_status,
        auditory_progress=new_test_session.auditory_progress,
        visual_progress=new_test_session.visual_progress,
        language_progress=new_test_session.language_progress,
        info=InfoSubmissionResponse.model_validate(new_test_session.human_feature)
    )
    
@router.get("/", response_model=list[TestStartResponse], response_model_exclude={'info'})
async def get_all_test_sessions_of_user(db: Session = Depends(get_db), current_participant=Depends(get_current_participant)):
    """
    Retrieve all test sessions for the current participant.
    """
    if current_participant.participant_type != ParticipantType.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can access their test sessions."
        )
        
    test_sessions = db.query(TestSession).filter(TestSession.participant_id == current_participant.id).all()
    if not test_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No test sessions found for the current participant."
        )
    return test_sessions

@router.post("/{test_session_id}/auditory", response_model=AuditorySubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_auditory_features(
    test_session_id: int,
    auditory_attributes: AuditorySubmissionRequest,
    db: Session = Depends(get_db),
    current_participant=Depends(get_current_participant)
) -> AuditorySubmissionResponse:
    """
    Submit auditory features for a specific test session.
    """
    test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.participant_id == current_participant.id).first()
    
    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test session not found."
        )
        
    if test_session.completion_status != TestStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test session is not in progress."
        )
    
    if auditory_attributes.question_type != test_session.auditory_progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auditory question type does not match the current progress."
        )
        
    auditory_feature = AuditoryFeatures(
        test_session_id=test_session_id,
        question_type=auditory_attributes.question_type,
        start_time=auditory_attributes.start_time,
        end_time=auditory_attributes.end_time,
        first_click_interval=auditory_attributes.first_click_interval,
        second_click_interval=auditory_attributes.second_click_interval,
        third_click_interval=auditory_attributes.third_click_interval,
        fourth_click_interval=auditory_attributes.fourth_click_interval,
        fifth_click_interval=auditory_attributes.fifth_click_interval,
        sixth_click_interval=auditory_attributes.sixth_click_interval,
        duration_from_round=auditory_attributes.duration_from_round,
        duration_from_interaction=auditory_attributes.duration_from_interaction,
        total_clicks=auditory_attributes.total_clicks,
        logic=auditory_attributes.logic,
        instructions_viewed=auditory_attributes.instructions_viewed
    )
    
    test_session.auditory_features.append(auditory_feature)
    test_session.auditory_progress = list(AuditoryProgress)[list(AuditoryProgress).index(auditory_attributes.question_type) + 1]
    
    db.add(auditory_feature)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This type of auditory feature has already been submitted for this test session."
        )
    db.refresh(auditory_feature)
    db.refresh(test_session)
    return AuditorySubmissionResponse.model_validate(auditory_feature)

@router.post("/{test_session_id}/visual", response_model=VisualSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_visual_features(
    test_session_id: int,
    visual_attributes: VisualSubmissionRequest,
    db: Session = Depends(get_db),
    current_participant=Depends(get_current_participant)
) -> VisualSubmissionResponse:
    """
    Submit visual features for a specific test session.
    """
    test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.participant_id == current_participant.id).first()
    
    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test session not found."
        )
        
    if test_session.completion_status != TestStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test session is not in progress."
        )
        
    if visual_attributes.question_type != test_session.visual_progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Visual question type does not match the current progress."
        )
        
    visual_feature = VisualFeatures(
        test_session_id=test_session_id,
        question_type=visual_attributes.question_type,
        start_time=visual_attributes.start_time,
        end_time=visual_attributes.end_time,
        total_clicks=visual_attributes.total_clicks,
        first_click_interval=visual_attributes.first_click_interval,
        second_click_interval=visual_attributes.second_click_interval,
        third_click_interval=visual_attributes.third_click_interval,
        fourth_click_interval=visual_attributes.fourth_click_interval,
        fifth_click_interval=visual_attributes.fifth_click_interval,
        sixth_click_interval=visual_attributes.sixth_click_interval,
        time_last_click=visual_attributes.time_last_click,
        correct_answers=visual_attributes.correct_answers,
        wrong_answers=visual_attributes.wrong_answers
    )
    
    test_session.visual_features.append(visual_feature)
    test_session.visual_progress = list(VisualProgress)[list(VisualProgress).index(visual_attributes.question_type) + 1]
    
    db.add(visual_feature)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This type of visual feature has already been submitted for this test session."
        )
    db.refresh(visual_feature)
    db.refresh(test_session)
    return VisualSubmissionResponse.model_validate(visual_feature)

@router.post("/{test_session_id}/language", response_model=LanguageSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_language_features(
    test_session_id: int,
    language_attributes: LanguageSubmissionRequest,
    db: Session = Depends(get_db),
    current_participant=Depends(get_current_participant)
) -> LanguageSubmissionResponse:
    """
    Submit language features for a specific test session.
    """
    test_session = db.query(TestSession).filter(TestSession.id == test_session_id, TestSession.participant_id == current_participant.id).first()
    
    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test session not found."
        )
        
    if test_session.completion_status != TestStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test session is not in progress."
        )
        
    if language_attributes.question_type != test_session.language_progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language question type does not match the current progress."
        )
        
    language_feature = LanguageFeatures(
        test_session_id=test_session_id,
        question_type=language_attributes.question_type,
        start_time=language_attributes.start_time,
        end_time=language_attributes.end_time,
        clicks=language_attributes.clicks,
        hits=language_attributes.hits,
        misses=language_attributes.misses
    )
    
    test_session.language_features.append(language_feature)
    test_session.language_progress = list(LanguageProgress)[list(LanguageProgress).index(language_attributes.question_type) + 1]

    db.add(language_feature)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This type of language feature has already been submitted for this test session."
        )
    db.refresh(language_feature)
    db.refresh(test_session)
    return LanguageSubmissionResponse.model_validate(language_feature)
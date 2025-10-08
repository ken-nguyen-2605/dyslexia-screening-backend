from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import TestResult, TestStatus, TestType
from app.models.test.auditory_test import AuditoryTest
from app.models.test.language_test import LanguageTest
from app.models.test.test_session import TestSession
from app.models.test.visual_test import VisualTest
from app.schemas.test_session import (
    SpecificTestSessionCreateSchema,
    SpecificTestSessionSchema,
    SpecificTestSessionSubmitSchema,
    TestSessionSchema,
)
from app.utils.auth import get_current_profile

router = APIRouter(
    prefix="/test-session",
    tags=["User - test session"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_profile)],
)


@router.get("/", response_model=list[TestSessionSchema], status_code=status.HTTP_200_OK)
async def get_all_test_sessions_of_user(
    db: Session = Depends(get_db), current_profile=Depends(get_current_profile)
):
    """Retrieve all test sessions for the current profile."""
    test_sessions = (
        db.query(TestSession).filter(TestSession.profile_id == current_profile.id).all()
    )
    return test_sessions


@router.get(
    "/{test_session_id}/",
    response_model=TestSessionSchema,
    status_code=status.HTTP_200_OK,
)
async def get_test_session_by_id(
    test_session_id: int,
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Retrieve a specific test session by its ID for the current profile."""
    test_session = (
        db.query(TestSession).filter(TestSession.id == test_session_id).first()
    )

    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test session not found."
        )

    if test_session.profile_id != current_profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this test session.",
        )

    return test_session


@router.post("/", response_model=TestSessionSchema, status_code=status.HTTP_201_CREATED)
async def start_test(
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Start a new test session for the current profile."""
    new_test_session = TestSession(
        profile_id=current_profile.id,
        completed=False,
    )

    db.add(new_test_session)
    db.commit()
    db.refresh(new_test_session)

    return new_test_session


@router.post(
    "/{test_session_id}/",
    response_model=SpecificTestSessionSchema,
    status_code=status.HTTP_201_CREATED,
)
async def start_specific_test(
    test_session_id: int,
    specific_test_request: SpecificTestSessionCreateSchema,
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Start a specific test (auditory, visual, language) within an existing test session."""
    test_session = (
        db.query(TestSession)
        .filter(
            TestSession.id == test_session_id,
            TestSession.profile_id == current_profile.id,
        )
        .first()
    )

    # Validate test session existence and status
    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test session not found."
        )

    if test_session.profile_id != current_profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to start a test in this session.",
        )

    if test_session.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test session is not in progress.",
        )

    match specific_test_request.test_type:
        case TestType.AUDITORY:
            if test_session.taken_auditory_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Auditory test has already been taken in this session.",
                )
            if test_session.auditory_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Auditory test has already been started in this session.",
                )
            auditory_test = AuditoryTest(
                test_session_id=test_session.id,
                score=None,
                test_details={},
            )
            test_session.auditory_test = auditory_test

        case TestType.VISUAL:
            if test_session.taken_visual_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Visual test has already been taken in this session.",
                )
            if test_session.visual_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Visual test has already been started in this session.",
                )
            visual_test = VisualTest(
                test_session_id=test_session.id,
                score=None,
                test_details={},
            )
            test_session.visual_test = visual_test

        case TestType.LANGUAGE:
            if test_session.taken_language_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Language test has already been taken in this session.",
                )
            if test_session.language_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Language test has already been started in this session.",
                )
            language_test = LanguageTest(
                test_session_id=test_session.id,
                score=None,
                test_details={},
            )
            test_session.language_test = language_test

        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid test type."
            )

    db.add(test_session)
    db.commit()
    db.refresh(test_session)

    match specific_test_request.test_type:
        case TestType.AUDITORY:
            return test_session.auditory_test
        case TestType.VISUAL:
            return test_session.visual_test
        case TestType.LANGUAGE:
            return test_session.language_test


@router.post(
    "/{test_session_id}/submit",
    status_code=status.HTTP_200_OK,
    response_model=SpecificTestSessionSchema,
)
async def submit_test(
    test_session_id: int,
    test_submission_request: SpecificTestSessionSubmitSchema,
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Submit answers for a specific test session."""
    test_session = (
        db.query(TestSession).filter(TestSession.id == test_session_id).first()
    )

    # Validate test session existence and status
    if not test_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test session not found."
        )
    if test_session.profile_id != current_profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to submit this test session.",
        )
    if test_session.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test session is not in progress.",
        )

    match test_submission_request.test_type:
        case TestType.AUDITORY:
            if not test_session.auditory_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Auditory test has not been started in this session.",
                )

            if test_session.taken_auditory_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Auditory test has already been submitted in this session.",
                )

            test_session.auditory_test.score = test_submission_request.score
            test_session.auditory_test.test_details = (
                test_submission_request.test_details
            )
            test_session.taken_auditory_test = True

        case TestType.VISUAL:
            if not test_session.visual_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Visual test has not been started in this session.",
                )
            if test_session.taken_visual_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Visual test has already been submitted in this session.",
                )
            test_session.visual_test.score = test_submission_request.score
            test_session.visual_test.test_details = test_submission_request.test_details
            test_session.taken_visual_test = True

        case TestType.LANGUAGE:
            if not test_session.language_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Language test has not been started in this session.",
                )
            if test_session.taken_language_test:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Language test has already been submitted in this session.",
                )
            test_session.language_test.score = test_submission_request.score
            test_session.language_test.test_details = (
                test_submission_request.test_details
            )
            test_session.taken_language_test = True

        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid test type."
            )

    if (
        test_session.taken_auditory_test
        and test_session.taken_visual_test
        and test_session.taken_language_test
    ):

        test_session.completed = True
        test_session.end_time = func.now()
        test_session.score, test_session.result = calc_overall_result(test_session)

    db.add(test_session)
    db.commit()
    db.refresh(test_session)

    match test_submission_request.test_type:
        case TestType.AUDITORY:
            return test_session.auditory_test
        case TestType.VISUAL:
            return test_session.visual_test
        case TestType.LANGUAGE:
            return test_session.language_test


def calc_overall_result(test_session: TestSession) -> tuple[float, TestResult]:
    """Calculate the overall result based on the scores of all tests."""
    average_score = (
        test_session.auditory_test.score
        + test_session.visual_test.score
        + test_session.language_test.score
    ) / 3

    if average_score >= 75:
        test_result = TestResult.NON_DYSLEXIC
    elif 50 <= average_score < 75:
        test_result = TestResult.MAYBE_DYSLEXIC
    else:
        test_result = TestResult.DYSLEXIC

    return average_score, test_result

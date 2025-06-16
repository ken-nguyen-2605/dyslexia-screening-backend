from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_participant
from app.models.test_session import TestSession
from app.models.enums import TestStatus, ParticipantType
from app.schemas.test_session import TestStartRequest, TestStartResponse

router = APIRouter(
    prefix="/test-session",
    tags=["test-session"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_participant)]
)

@router.post("/", response_model=TestStartResponse)
async def start_test(db: Session = Depends(get_db), current_participant=Depends(get_current_participant)):
    """
    Start a new test session for the current participant.
    """
    new_test_session = TestSession(
        completion_status=TestStatus.IN_PROGRESS,
        participant=current_participant
    )
        
    db.add(new_test_session)
    db.commit()
    db.refresh(new_test_session)
    
    return TestStartResponse(
        test_id=new_test_session.id,
        participant_id=new_test_session.participant_id,
        start_time=new_test_session.start_time,
        completion_status=new_test_session.completion_status
    )
    
@router.get("/", response_model=list[TestStartResponse])
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
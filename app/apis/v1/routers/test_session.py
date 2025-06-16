from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_participant
from app.models.test_session import TestSession
from app.models.enums import TestStatus
from app.schemas.test_session import TestStartRequest, TestStartResponse

router = APIRouter(
    prefix="/test-session",
    tags=["test-session"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_participant)]
)

@router.post("/start", response_model=TestStartResponse, status_code=status.HTTP_200_OK)
async def start_test(db: Session = Depends(get_db), current_participant=Depends(get_current_participant)):
    new_test_session = TestSession(
        participant_id=current_participant.id,
        completion_status=TestStatus.IN_PROGRESS,
        participant=current_participant
    )
    
    db.add(new_test_session)
    db.commit()
    db.refresh(new_test_session)
    return TestStartResponse(
        test_id=str(new_test_session.id),
        start_time=new_test_session.start_time,
        completion_status=new_test_session.completion_status
    )
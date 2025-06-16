from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_participant

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_participant)]
)

@router.post("/start")
async def start_test(db: Session = Depends(get_db), current_participant=Depends(get_current_participant)):
    """
    Endpoint to start a test. It returns the current participant's information.
    """
    
    
    return {
        "message": "Test started successfully",
        "participant": current_participant
    }
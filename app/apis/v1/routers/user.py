from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.utils.auth import get_current_participant

from app.schemas.user import ProfileResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_participant)]
)

# @router.get("/profile", response_model=ProfileResponse)
# async def get_profile(db: Session = Depends(get_db), current_participant: Participant = Depends(get_current_participant)) -> ProfileResponse:
#     """
#     Get the profile of the current user.
#     """
#     try:
#         user_participant = db.query(UserParticipant).filter(
#             UserParticipant.participant_id == current_participant.id
#         ).first()
            
#         if not user_participant:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
#         return ProfileResponse(
#             id=current_participant.id,
#             name=user_participant.name,
#             email=current_participant.email,
#             created_at=current_participant.created_at
#         )
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
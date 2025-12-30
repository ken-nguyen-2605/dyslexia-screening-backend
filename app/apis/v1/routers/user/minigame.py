"""This router handles minigame attempts submitted by users."""

from fastapi import APIRouter, HTTPException, Query
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_profile
from app.models.minigame.minigame import Minigame, MinigameNumber
from app.schemas.minigame import MinigameCreate, MinigameResponse

router = APIRouter(
    prefix="/minigame",
    tags=["User - minigame"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_profile)],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[MinigameResponse])
async def get_all_minigames(
    minigame_number: MinigameNumber | None = Query(default=None, description="Filter by minigame number"),
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Retrieve all minigame attempts for the current profile, optionally filtered by minigame number."""
    query = db.query(Minigame).filter(Minigame.profile_id == current_profile.id)
    
    if minigame_number:
        query = query.filter(Minigame.minigame_number == minigame_number)
    
    minigames = query.all()
    return minigames


@router.get("/{minigame_id}", status_code=status.HTTP_200_OK, response_model=MinigameResponse)
async def get_minigame(
    minigame_id: int,
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Retrieve a specific minigame attempt by ID for the current profile."""
    minigame = (
        db.query(Minigame)
        .filter(Minigame.id == minigame_id, Minigame.profile_id == current_profile.id)
        .first()
    )
    if not minigame:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Minigame attempt not found",
        )
    return minigame


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MinigameResponse)
async def submit_minigame(
    minigame_data: MinigameCreate,
    db: Session = Depends(get_db),
    current_profile=Depends(get_current_profile),
):
    """Submit a new minigame attempt for the current profile."""
    new_minigame = Minigame(
        minigame_number=minigame_data.minigame_number,
        score=minigame_data.score,
        minigame_details=minigame_data.minigame_details,
        attempted_at=minigame_data.attempted_at,
        profile_id=current_profile.id,
    )
    db.add(new_minigame)
    db.commit()
    db.refresh(new_minigame)
    return new_minigame
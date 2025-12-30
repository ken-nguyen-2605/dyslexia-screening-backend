from enum import StrEnum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import TIMESTAMP, func
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class MinigameNumber(StrEnum):
    ONE = "one"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"

class Minigame(Base):
    __tablename__ = "minigames"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    minigame_number: Mapped[MinigameNumber] = mapped_column(Enum(MinigameNumber), nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    score: Mapped[float] = mapped_column(nullable=False)  # Over 5
    minigame_details: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Relationships
    profile_id: Mapped[int] = mapped_column(nullable=False)

"""
Example JSON minigame_details structure:
{
    "failed_questions": [
        {
            "question_id": 1,
            "user_answer": "B",
            "correct_answer": "C"
        },
        {
            "question_id": 3,
            "user_answer": "A",
            "correct_answer": "D"
        }
    ],
}
"""
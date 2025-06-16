from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class UserParticipant(Base):
    __tablename__ = 'user_participants'
    
    participant_id: Mapped[int] = mapped_column(ForeignKey('participants.id'), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    
    participant: Mapped["Participant"] = relationship("Participant", back_populates="user_participant")  # type: ignore
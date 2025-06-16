from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from sqlalchemy import Enum
from .enums import ParticipantType  # Assuming you have an Enum defined for participant types

class Participant(Base):
    __tablename__ = 'participants'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    participant_type: Mapped[ParticipantType] = mapped_column(Enum(ParticipantType), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user_participant: Mapped["UserParticipant"] = relationship("UserParticipant", back_populates="participant", uselist=False)  # type: ignore
    guest_participant: Mapped["GuestParticipant"] = relationship("GuestParticipant", back_populates="participant", uselist=False)  # type: ignore
    test_sessions: Mapped["TestSession"] = relationship("TestSession", back_populates="participant")  # type: ignore
    session_contexts: Mapped["SessionContext"] = relationship("SessionContext", back_populates="participant")  # type: ignore
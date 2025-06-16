from datetime import datetime
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class GuestParticipant(Base):
    __tablename__ = 'guest_participants'

    participant_id: Mapped[int] = mapped_column(ForeignKey('participants.id'), primary_key=True, autoincrement=True)
    last_activity: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    
    participant: Mapped["Participant"] = relationship(back_populates="guest_participant", uselist=False)  # type: ignore
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class GuestParticipant(Base):
    __tablename__ = 'guest_participants'

    participant_id = Column(Integer, ForeignKey('participants.id'), primary_key=True, autoincrement=True)
    guest_token = Column(String(128), nullable=False, unique=True)
    last_activity = Column(TIMESTAMP(timezone=True), nullable=True)
    
    participant = relationship("Participant", back_populates="guest_participant")
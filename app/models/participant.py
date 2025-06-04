from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import Enum
from .enums import ParticipantTypeEnum  # Assuming you have an Enum defined for participant types

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_type = Column(Enum(ParticipantTypeEnum), nullable=False) 
    email = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships
    user_participant = relationship("UserParticipant", back_populates="participant", uselist=False)
    guest_participant = relationship("GuestParticipant", back_populates="participant", uselist=False)
    test_sessions = relationship("TestSession", back_populates="participant")
    session_contexts = relationship("SessionContext", back_populates="participant")

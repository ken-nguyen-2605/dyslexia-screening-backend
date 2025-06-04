from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserParticipant(Base):
    __tablename__ = 'user_participants'

    participant_id = Column(Integer, ForeignKey('participants.id'), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    
    participant = relationship("Participant", back_populates="user_participant")
    
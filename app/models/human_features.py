from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class HumanFeatures(Base):
    __tablename__ = 'human_features'

    id = Column(Integer, primary_key=True)
    test_session_id = Column(Integer, ForeignKey('test_session.id'))

    age = Column(Integer)
    gender = Column(String)
    native_language = Column(String)
    rl_dyslexia = Column(Boolean)
    has_played_similar_game = Column(Boolean)

    visual_rating = Column(Integer)
    audio_rating = Column(Integer)
    language_rating = Column(Integer)

    test_session = relationship("TestSession", back_populates="human_features")
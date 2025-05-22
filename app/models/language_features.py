from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class LanguageFeatures(Base):
    __tablename__ = 'language_features'

    id = Column(Integer, primary_key=True)
    test_session_id = Column(Integer, ForeignKey('test_session.id'))

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    clicks = Column(Integer)
    hits = Column(Integer)
    misses = Column(Integer)

    test_session = relationship("TestSession", back_populates="language_features")
from sqlalchemy import Column, Integer, Boolean, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class TestSession(Base):
    __tablename__ = 'test_session'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    start_time = Column(TIMESTAMP, server_default=func.now())
    end_time = Column(TIMESTAMP)
    completion_status = Column(String(20), nullable=False)  # e.g., 'completed', 'in_progress'
    predict_dyslexia = Column(Boolean)

    # Relationships
    account = relationship("Account", back_populates="test_sessions")
    user_contexts = relationship("UserContext", back_populates="test_session")
    # One-to-one relationships with feature models
    human_features = relationship("HumanFeatures", uselist=False, back_populates="test_session")
    visual_features = relationship("VisualFeatures", uselist=False, back_populates="test_session")
    auditory_features = relationship("AuditoryFeatures", uselist=False, back_populates="test_session")
    language_features = relationship("LanguageFeatures", uselist=False, back_populates="test_session")
from sqlalchemy import Column, Integer, TIMESTAMP, Interval, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class VisualFeatures(Base):
    __tablename__ = 'visual_features'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_session_id = Column(Integer, ForeignKey('test_sessions.id'))

    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    total_clicks = Column(Integer)

    first_click_interval = Column(Interval)
    second_click_interval = Column(Interval)
    third_click_interval = Column(Interval)
    fourth_click_interval = Column(Interval)
    fifth_click_interval = Column(Interval)
    sixth_click_interval = Column(Interval)
    time_last_click = Column(Interval)

    correct_answers = Column(Integer)
    wrong_answers = Column(Integer)

    test_session = relationship("TestSession", back_populates="visual_features")
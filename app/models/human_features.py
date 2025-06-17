from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import Gender

class HumanFeatures(Base):
    __tablename__ = 'human_features'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(ForeignKey('test_sessions.id'))
    
    # Before starting the test
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    native_language: Mapped[str] = mapped_column(String(50), nullable=False)
    rl_dyslexia: Mapped[bool] = mapped_column(nullable=False)
    
    # After completing the test
    has_played_similar_game: Mapped[bool | None] = mapped_column()
    auditory_rating: Mapped[int | None] = mapped_column()
    visual_rating: Mapped[int | None] = mapped_column()
    language_rating: Mapped[int | None] = mapped_column()

    test_session: Mapped["TestSession"] = relationship(back_populates="human_feature")  # type: ignore
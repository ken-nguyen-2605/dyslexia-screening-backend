from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class VisualTest(Base):
    __tablename__ = "visual_tests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_session_id: Mapped[int] = mapped_column(
        ForeignKey("test_sessions.id"), nullable=False
    )
    score: Mapped[float] = mapped_column(nullable=True)  # Over 100
    test_details: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Relationships
    test_session: Mapped["TestSession"] = relationship(back_populates="visual_test")  # type: ignore

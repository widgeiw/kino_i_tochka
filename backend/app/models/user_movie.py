from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Identity,
    func,
    Index
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class UserMovie(Base):
    __tablename__ = "user_movies"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    movie_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("movies.id", ondelete="CASCADE"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('watched', 'want_to_watch')",
            name="user_movies_status_check",
        ),
        UniqueConstraint(
            "user_id",
            "movie_id",
            name="uq_user_movie",
        ),
        Index("idx_user_movies_movie_id", "movie_id"),
        Index("idx_user_movies_status", "status"),
        Index("idx_user_movies_user_id", "user_id"),
    )
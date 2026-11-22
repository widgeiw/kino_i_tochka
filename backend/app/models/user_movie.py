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
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


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
    )
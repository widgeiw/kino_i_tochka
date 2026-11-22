from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    SmallInteger,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Text,
    Identity,
    func,
    Index
    )
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

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

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    review_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 10",
            name="reviews_rating_check",
        ),
        UniqueConstraint(
            "user_id",
            "movie_id",
            name="uq_user_movie_review",
        ),
        Index(
            "idx_reviews_user_id",
            "user_id"
        ),
        Index(
            "idx_reviews_movie_id",
            "movie_id"
        )
    )
from sqlalchemy import (
    BigInteger,
    DateTime, 
    String, 
    Integer, 
    func,
    CheckConstraint, 
    Identity, 
    Text, 
    Numeric, 
    Date,
    Index
    )

from sqlalchemy.orm import Mapped, mapped_column

from datetime import date, datetime

from app.core.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    tmdb_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    overview: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    release_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    vote_average: Mapped[float | None] = mapped_column(
        Numeric(3, 1),
        nullable=True,
    )

    poster_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    runtime: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        
    )

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint("runtime IS NULL OR runtime > 0", name="movies_runtime_check"),
        CheckConstraint("vote_average BETWEEN 0 AND 10", name="movies_vote_average_check"),
        Index("idx_movies_title", "title"),
    )

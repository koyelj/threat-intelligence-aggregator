from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Feed(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    feed_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    feed_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active"
    )

    last_updated: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class IOC(Base):
    __tablename__ = "iocs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True
    )

    ioc_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    source_feed_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    confidence: Mapped[str] = mapped_column(
        String(20),
        default="Medium"
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        default="Low"
    )

    occurrence_count: Mapped[int] = mapped_column(
        default=1
    )
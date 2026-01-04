import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseDatabaseContext:
    """Generic Asynchronous context manager for Database sessions."""

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self) -> AsyncSession:
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.commit()
            await self.session.close()


async def generic_get_db(session_factory) -> AsyncGenerator[AsyncSession, None]:
    """Generic generator to yield a database session."""
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


NAMING_CONVENTION = {
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s',
    'pk': 'pk_%(table_name)s',
}


class UUIDMixin:
    """Standard ID column."""

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(),
        primary_key=True,
        default=uuid.uuid4,
        server_default=sa.text('gen_random_uuid()'),
    )


class SharedModel(DeclarativeBase, UUIDMixin):
    __abstract__ = True


class OrderPositionMixin:
    """Order position column."""

    order_position: Mapped[int] = mapped_column(nullable=False, index=True)


class SharedOrderedModel(SharedModel, OrderPositionMixin):
    """Base class for ordered database models."""

    __abstract__ = True


class DateAuditMixin:
    """Created and Updated date columns."""

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        default=lambda: datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        default=lambda: datetime.now(UTC),
    )

import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from rssa_storage.shared import DateAuditMixin
from rssa_storage.shared.db_utils import NAMING_CONVENTION, SharedModel


class MovieBase(SharedModel, DateAuditMixin):
    __abstract__ = True

    metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)


class MovieForeignKeyMixin:
    """Adds the movie_id foreign key column."""

    movie_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('movies.id'),
        index=True,
        nullable=False,
    )

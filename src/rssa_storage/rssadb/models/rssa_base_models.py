"""SQLAlchemy base models for the RSSA API."""

import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from rssa_storage.shared.db_utils import NAMING_CONVENTION, SharedModel, SharedOrderedModel


class RssaBase(SharedModel):
    __abstract__ = True

    metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)


class RssaOrderedBase(SharedOrderedModel):
    __abstract__ = True

    metadata = RssaBase.metadata


class StudyParticipantContextMixin:
    """Mixin class to add study participant context fields to models.

    Attributes:
        study_id: Foreign key to the study.
        study_step_id: Foreign key to the study step.
        study_step_page_id (Optional[uuid.UUID]): Foreign key to the step page.
        study_participant_id: Foreign key to the study participant.
        context_tag: Context tag for the response.
        version: Version of the response.
        discarded: Indicates if the response is discarded.
    """

    __abstract__ = True
    study_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('studies.id'),
        nullable=False,
    )
    study_step_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('study_steps.id'),
        nullable=False,
    )
    study_step_page_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('study_step_pages.id'),
        nullable=True,
    )
    study_participant_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('study_participants.id'),
        nullable=False,
    )
    context_tag: Mapped[str] = mapped_column(nullable=False)
    version: Mapped[int] = mapped_column(default=1, server_default=sa.text('1'))
    discarded: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False, server_default=sa.text('FALSE'))


class DBBaseParticipantResponseModel(RssaBase, StudyParticipantContextMixin):
    """Base class for participant response models in the RSSA API.

    Attributes:
        Inherits id, study participant context fields from parent classes.
    """

    __abstract__ = True

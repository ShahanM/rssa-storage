"""SQLAlchemy models for participant movie sequences in the RSSA API."""

import random
import uuid
from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rssa_storage.rssadb.models.rssa_base_models import RssaBase
from rssa_storage.shared import DateAuditMixin, SoftDeleteMixin


def generate_seed():
    return random.randint(0, 2147483647)


class PreShuffledMovieList(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'pre_shuffled_movie_lists' table.

    Stores pre-generated, fully shuffled lists of movie UUIDs.

    Attributes:
        list_id (int): Primary key, auto-incremented.
        movie_ids (List[uuid.UUID]): Ordered list of movie UUIDs.
        subset_desc (str): Description of the movie subset.
        seed (int): Seed used for shuffling.
        created_at (datetime): Timestamp of creation.
    """

    __tablename__ = 'pre_shuffled_movie_lists'

    movie_ids: Mapped[list[uuid.UUID]] = mapped_column(sa.ARRAY(sa.UUID()), nullable=False)
    subset_desc: Mapped[str | None] = mapped_column(sa.Text)
    seed: Mapped[int] = mapped_column(default=generate_seed)

    def __repr__(self):
        """String representation of PreShuffledMovieList."""
        return f'<PreShuffledMovieList(list_id={self.id}, num_movies={len(self.movie_ids) if self.movie_ids else 0})>'


class StudyParticipantMovieSession(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'study_participant_movie_sessions' table.

    Tracks each participant's assigned movie list and their current progress.

    Attributes:
        study_participant_id (uuid.UUID): Primary key, references the participant.
        assigned_list_id (int): Foreign key to the assigned pre-shuffled movie list.
        current_offset (int): Current position in the movie list.
        created_at (datetime): Timestamp of session creation.
        last_accessed_at (datetime): Timestamp of last access to the session.
    """

    __tablename__ = 'study_participant_movie_sessions'

    study_participant_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('study_participants.id', ondelete='CASCADE'), nullable=False
    )
    assigned_list_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('pre_shuffled_movie_lists.id', ondelete='CASCADE'), nullable=False
    )
    current_offset: Mapped[int] = mapped_column(server_default=sa.text('0'), nullable=False)

    last_accessed_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        default=lambda: datetime.now(UTC),
    )

    assigned_list: Mapped[PreShuffledMovieList] = relationship(PreShuffledMovieList, lazy='joined')

    def __repr__(self):
        """String representation of ParticipantMovieSession."""
        return (
            f'<ParticipantMovieSession(study_participant_id={self.study_participant_id}, '
            f'assigned_list_id={self.assigned_list_id}, offset={self.current_offset})>'
        )

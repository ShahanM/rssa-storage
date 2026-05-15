"""Repository related to StudyParticipant models."""

import uuid
from typing import Any

from sqlalchemy import Row, and_, func, select
from sqlalchemy.orm import selectinload

from rssa_storage.rssadb.models.participant_movie_sequence import StudyParticipantMovieSession
from rssa_storage.rssadb.models.study_participants import (
    Demographic,
    ParticipantRecommendationContext,
    ParticipantStudySession,
    StudyParticipant,
)
from rssa_storage.shared import BaseRepository, RepoQueryOptions
from rssa_storage.shared.mixins import VersionedRepositoryMixin


class StudyParticipantRepository(BaseRepository[StudyParticipant]):
    """Repository for StudyParticipant model."""

    SEARCHABLE_COLUMNS = ['id', 'prolific_pid']
    LOAD_ASSIGNED_CONDITION = (selectinload(StudyParticipant.study_condition),)


class ParticipantRecommendationContextRepository(BaseRepository[ParticipantRecommendationContext]):
    """Repository for ParticipantRecommendationContext model."""

    pass


class ParticipantStudySessionRepository(BaseRepository[ParticipantStudySession]):
    """Repository for ParticipantStudySession model."""

    pass


class StudyParticipantMovieSessionRepository(BaseRepository[StudyParticipantMovieSession]):
    """Repository for ParticipantMovieSession model."""

    async def get_movie_session_by_participant_id(
        self, participant_id: uuid.UUID
    ) -> StudyParticipantMovieSession | None:
        """Get ParticipantMovieSession by participant ID.

        Args:
            participant_id: The UUID of the study participant.

        Returns:
            The ParticipantMovieSession instance or None if not found.
        """
        return await self.find_one(RepoQueryOptions(filters={'study_participant_id': participant_id}))


class ParticipantDemographicRepository(BaseRepository[Demographic], VersionedRepositoryMixin):
    """Repository for managing Demographic entities in the database.

    Inherits from BaseRepository to provide CRUD operations for Demographic model.

    Attributes:
        db (AsyncSession): The asynchronous database session.
    """

    async def get_aggregate_distribution(
        self, study_id: uuid.UUID, demographic_field: str, verified_participants_only: bool = False
    ) -> list[Row[tuple[Any, int]]]:
        """
        Get aggregate counts for a specific demographic field within a study.
        """
        target_column = getattr(self.model, demographic_field)

        join_conditions = [
            StudyParticipant.id == Demographic.study_participant_id,
            StudyParticipant.study_id == study_id,
            StudyParticipant.discarded.is_(False),
        ]

        if verified_participants_only:
            join_conditions.append(StudyParticipant.is_verified.is_(True))

        query = (
            select(target_column.label('category'), func.count(Demographic.id).label('count'))
            .join(
                StudyParticipant,
                and_(*join_conditions),
            )
            .where(StudyParticipant.discarded.is_(False))
            .group_by(target_column)
            .order_by(func.count(StudyParticipant.id).desc())
        )

        query = self._apply_soft_delete_filter(query)

        result = await self.db.execute(query)
        return list(result.all())

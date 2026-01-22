"""Repository related to StudyParticipant models."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from rssa_storage.rssadb.models.participant_movie_sequence import StudyParticipantMovieSession
from rssa_storage.rssadb.models.study_participants import (
    Demographic,
    ParticipantRecommendationContext,
    ParticipantStudySession,
    StudyParticipant,
    StudyParticipantType,
)
from rssa_storage.shared import BaseRepository, RepoQueryOptions
from rssa_storage.shared.mixins import VersionedRepositoryMixin


class StudyParticipantRepository(BaseRepository[StudyParticipant]):
    """Repository for StudyParticipant model."""

    LOAD_ASSIGNED_CONDITION = (selectinload(StudyParticipant.study_condition),)
    LOAD_CONDITION_AND_TYPE = (
        selectinload(StudyParticipant.study_condition),
        selectinload(StudyParticipant.study_participant_type),
    )


class StudyParticipantTypeRepository(BaseRepository[StudyParticipantType]):
    """Repository for StudyParticipantType model."""

    pass


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

    pass

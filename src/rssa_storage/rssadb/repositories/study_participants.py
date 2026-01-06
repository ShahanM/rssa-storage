"""Repository related to StudyParticipant models."""

import uuid
from typing import Any

from sqlalchemy import MergedResult, select, update
from sqlalchemy.orm import selectinload

from rssa_storage.rssadb.models.participant_movie_sequence import StudyParticipantMovieSession
from rssa_storage.rssadb.models.study_participants import (
    Demographic,
    ParticipantRecommendationContext,
    ParticipantStudySession,
    StudyParticipant,
    StudyParticipantType,
)
from rssa_storage.shared import BaseRepository


class StudyParticipantRepository(BaseRepository[StudyParticipant]):
    LOAD_ASSIGNED_CONDITION = (selectinload(StudyParticipant.study_condition),)


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
        query = select(StudyParticipantMovieSession).where(
            StudyParticipantMovieSession.study_participant_id == participant_id
        )

        db_row = await self.db.execute(query)

        return db_row.scalar_one_or_none()


class ParticipantDemographicRepository(BaseRepository[Demographic]):
    """Repository for managing Demographic entities in the database.

    Inherits from BaseRepository to provide CRUD operations for Demographic model.

    Attributes:
        db (AsyncSession): The asynchronous database session.
    """

    async def update_response(self, item_id: uuid.UUID, update_payload: dict[str, Any], client_version: int) -> bool:
        """Update a Demographic entry with optimistic concurrency control.

        Args:
            item_id: The UUID of the Demographic entry to update.
            update_payload: The fields to update with their new values.
            client_version: The version of the entry as known by the client.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        update_fields = {**update_payload, 'version': client_version + 1}
        update_stmt = (
            update(Demographic)
            .where(Demographic.id == item_id, Demographic.version == client_version)
            .values(**update_fields)
        )

        result = await self.db.execute(update_stmt)

        if isinstance(result, MergedResult):
            if result.rowcount == 1:
                await self.db.commit()
                return True

        await self.db.rollback()
        return False

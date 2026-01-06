"""Repository for participant responses."""

import uuid
from typing import TypeVar

from sqlalchemy import update

from rssa_storage.rssadb.models.participant_responses import (
    ParticipantFreeformResponse,
    ParticipantInteractionLog,
    ParticipantRating,
    ParticipantStudyInteractionResponse,
    ParticipantSurveyResponse,
)
from rssa_storage.rssadb.models.rssa_base_models import DBBaseParticipantResponseModel
from rssa_storage.shared import BaseRepository

ModelType = TypeVar('ModelType', bound=DBBaseParticipantResponseModel)


class BaseParticipantResponseRepository(BaseRepository[ModelType]):
    """Base repository for participant responses.

    Inherits from BaseRepository to provide CRUD operations for participant response models.

    Attributes:
        db: The database session.
        model: The participant response model class.
    """

    async def update_response(self, instance_id: uuid.UUID, update_data: dict, client_version: int) -> bool:
        """Update a participant response with optimistic concurrency control.

        Args:
            instance_id: The UUID of the participant response to update.
            update_data: A dictionary of fields to update.
            client_version: The version number provided by the client.

        Returns:
            True if the update was successful, False if there was a version conflict.
        """
        update_fields = {**update_data, 'version': client_version + 1}
        update_stmt = (
            update(self.model)
            .where(self.model.id == instance_id, self.model.version == client_version)
            .values(**update_fields)
        )

        result = await self.db.execute(update_stmt)
        if result.rowcount == 1:  # type: ignore
            await self.db.flush()
            return True
        else:
            await self.db.rollback()
            return False


class ParticipantSurveyResponseRepository(BaseParticipantResponseRepository[ParticipantSurveyResponse]):
    """Repository for ParticipantSurveyResponse model."""

    pass


class ParticipantFreeformResponseRepository(BaseParticipantResponseRepository[ParticipantFreeformResponse]):
    """Repository for FreeformResponse model."""

    pass


class ParticipantRatingRepository(BaseParticipantResponseRepository[ParticipantRating]):
    """Repository for ParticipantRating model."""

    pass


class ParticipantInteractionLogRepository(BaseRepository[ParticipantInteractionLog]):
    """Repository for ParticipantInteractionLog model."""

    pass


class ParticipantStudyInteractionResponseRepository(
    BaseParticipantResponseRepository[ParticipantStudyInteractionResponse]
):
    """Repository for ParticipantStudyInteractionResponse model."""

    pass

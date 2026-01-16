"""Repository for participant responses."""

from typing import TypeVar

from rssa_storage.rssadb.models.participant_responses import (
    ParticipantFreeformResponse,
    ParticipantInteractionLog,
    ParticipantRating,
    ParticipantStudyInteractionResponse,
    ParticipantSurveyResponse,
)
from rssa_storage.rssadb.models.rssa_base_models import DBBaseParticipantResponseModel
from rssa_storage.shared import BaseRepository
from rssa_storage.shared.mixins import VersionedRepositoryMixin

ModelType = TypeVar('ModelType', bound=DBBaseParticipantResponseModel)


class BaseParticipantResponseRepository(BaseRepository[ModelType], VersionedRepositoryMixin):
    """Base repository for participant responses.

    Inherits from BaseRepository to provide CRUD operations for participant response models.

    Attributes:
        db: The database session.
        model: The participant response model class.
    """

    pass


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

"""Repository for user operations."""

import uuid

from sqlalchemy import select

from rssa_storage.rssadb.models.participant_movie_sequence import PreShuffledMovieList
from rssa_storage.rssadb.models.study_components import ApiKey, User
from rssa_storage.shared import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    SEARCHABLE_COLUMNS = ['email', 'auth0_sub', 'desc']


class ApiKeyRepository(BaseRepository[ApiKey]):
    """Repository for ApiKey model."""

    async def get_active_api_key_with_study(self, key_hash: str, study_id: uuid.UUID) -> ApiKey | None:
        """Get an active API key by its hash and associated study ID."""
        query = select(ApiKey).join(ApiKey.study).where(ApiKey.is_active, ApiKey.study_id == study_id)
        result = await self.db.execute(query)

        return result.scalar_one_or_none()


class PreShuffledMovieRepository(BaseRepository[PreShuffledMovieList]):
    """Repository for PreShuffledMovieList model."""

    pass

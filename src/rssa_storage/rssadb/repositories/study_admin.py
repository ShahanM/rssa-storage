"""Repository for user operations."""

import uuid

from sqlalchemy import select

from rssa_storage.rssadb.models.participant_movie_sequence import PreShuffledMovieList
from rssa_storage.rssadb.models.study_components import ApiKey, User
from rssa_storage.shared import BaseRepository, RepoQueryOptions


class UserRepository(BaseRepository[User]):
    """Repository for User model."""


class ApiKeyRepository(BaseRepository[ApiKey]):
    """Repository for ApiKey model."""

    async def get_active_api_key_with_study(self, key_hash: str, study_id: uuid.UUID) -> ApiKey | None:
        """Get an active API key by its hash and associated study ID.

        Args:
            key_hash: The hash of the API key.
            study_id: The UUID of the associated study.

        Returns:
            The ApiKey instance if found, else None.
        """
        query = select(ApiKey).join(ApiKey.study).where(ApiKey.is_active, ApiKey.study_id == study_id)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()


class PreShuffledMovieRepository(BaseRepository[PreShuffledMovieList]):
    """Repository for PreShuffledMovieList model."""

    async def get_all_shuffled_lists_by_subset(self, subset_desc: str) -> list[PreShuffledMovieList]:
        """Get all pre-shuffled movie lists by subset description.

        Args:
            subset_desc: The subset description to filter by.

        Returns:
            A list of PreShuffledMovieList instances or an empty list.
        """
        movie_list = await self.find_many(RepoQueryOptions(filters={'subset_desc': subset_desc}))
        return list(movie_list)

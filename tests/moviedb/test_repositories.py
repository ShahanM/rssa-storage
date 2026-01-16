import unittest
import uuid
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import String, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rssa_storage.moviedb.repositories.movies import MovieRepository


# Simple Declarative Base for testing
class Base(DeclarativeBase):
    pass


class SimpleMovie(Base):
    __tablename__ = 'movies'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)


class TestMovieRepository(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_result = MagicMock()
        self.mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = self.mock_result

        # We use a repository instance with our SimpleMovie model to avoid importing the complex real model
        # which might have dependencies or complex relationships not needed for this unit test.
        # However, the real Repository imports the real Model type hint.

        self.repo = MovieRepository(db=self.mock_db, model=SimpleMovie)

    async def test_get_by_similarity(self):
        await self.repo.get_by_similarity(field_name='title', query_str='test')
        self.mock_db.execute.assert_called_once()

    async def test_get_by_prefix(self):
        await self.repo.get_by_prefix(field_name='title', prefix='test')
        self.mock_db.execute.assert_called_once()

    async def test_get_by_exact_ilike(self):
        await self.repo.get_by_exact_ilike(field_name='title', value='test')
        self.mock_db.execute.assert_called_once()

    async def test_get_by_similarity_invalid_field(self):
        with self.assertRaises(AttributeError):
            await self.repo.get_by_similarity(field_name='invalid_field', query_str='test')

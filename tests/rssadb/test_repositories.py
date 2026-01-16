import unittest
import uuid
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import Integer, String, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rssa_storage.rssadb.repositories.participant_responses import ParticipantSurveyResponseRepository
from rssa_storage.rssadb.repositories.study_admin import ApiKeyRepository
from rssa_storage.rssadb.repositories.study_components import StudyStepRepository
from rssa_storage.rssadb.repositories.study_participants import StudyParticipantMovieSessionRepository


# We need a Mixin to satisfy VersionedRepositoryMixin protocol if we mock models
# But for tests it's better to use real models or a local Declarative base
class Base(DeclarativeBase):
    pass


class MockParticipantResponse(Base):
    __tablename__ = 'mock_participant_response'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    version: Mapped[int] = mapped_column(Integer, default=1)


class MockStudyStep(Base):
    __tablename__ = 'mock_study_step'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    study_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    path: Mapped[str] = mapped_column(String)


class MockApiKey(Base):
    __tablename__ = 'mock_api_key'
    key_hash: Mapped[str] = mapped_column(String, primary_key=True)
    study_id: Mapped[uuid.UUID] = mapped_column(Uuid)


class TestRSSADBRepositories(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_result = MagicMock()
        self.mock_result.scalars.return_value.all.return_value = []
        self.mock_result.scalars.return_value.first.return_value = None
        self.mock_result.scalar_one_or_none.return_value = None
        self.mock_result.rowcount = 1  # Default success for updates
        self.mock_db.execute.return_value = self.mock_result

    async def test_versioned_mixin_update_success(self):
        repo = ParticipantSurveyResponseRepository(db=self.mock_db, model=MockParticipantResponse)
        instance_id = uuid.uuid4()
        update_data = {'response': 'new'}
        client_version = 1

        success = await repo.update_response(instance_id, update_data, client_version)

        self.assertTrue(success)
        self.mock_db.execute.assert_called_once()
        self.mock_db.flush.assert_called_once()

    async def test_versioned_mixin_update_conflict(self):
        repo = ParticipantSurveyResponseRepository(db=self.mock_db, model=MockParticipantResponse)

        # Mock 0 rows affected
        self.mock_db.execute.return_value.rowcount = 0

        instance_id = uuid.uuid4()
        update_data = {'response': 'new'}
        client_version = 1

        success = await repo.update_response(instance_id, update_data, client_version)

        self.assertFalse(success)
        self.mock_db.rollback.assert_called_once()

    async def test_validate_path_uniqueness(self):
        repo = StudyStepRepository(db=self.mock_db, model=MockStudyStep)
        study_id = uuid.uuid4()

        # Case 1: Unique (no result found)
        self.mock_db.execute.return_value.first.return_value = None
        is_unique = await repo.validate_path_uniqueness(study_id, 'new-path')
        self.assertTrue(is_unique)

        # Case 2: Not unique (result found)
        self.mock_db.execute.return_value.first.return_value = MockStudyStep()
        is_unique = await repo.validate_path_uniqueness(study_id, 'existing-path')
        self.assertFalse(is_unique)

    async def test_get_active_api_key(self):
        repo = ApiKeyRepository(db=self.mock_db, model=MockApiKey)
        study_id = uuid.uuid4()

        mock_key = MockApiKey(key_hash='hash', study_id=study_id)
        self.mock_db.execute.return_value.scalar_one_or_none.return_value = mock_key

        result = await repo.get_active_api_key_with_study('some-hash', study_id)
        self.assertEqual(result, mock_key)

    async def test_get_movie_session(self):
        class MockSessionModel(Base):
            __tablename__ = 'mock_session'
            id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
            study_participant_id: Mapped[uuid.UUID] = mapped_column(Uuid)

        repo = StudyParticipantMovieSessionRepository(db=self.mock_db, model=MockSessionModel)

        await repo.get_movie_session_by_participant_id(uuid.uuid4())
        self.mock_db.execute.assert_called_once()

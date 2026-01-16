import unittest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rssa_storage.shared import BaseRepository, RepoQueryOptions


class Base(DeclarativeBase):
    pass


class SimpleModel(Base):
    __tablename__ = 'test_model'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class TestBaseRepo(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        # Mock execute result
        self.mock_result = MagicMock()
        self.mock_result.scalars.return_value.all.return_value = []
        self.mock_result.scalars.return_value.first.return_value = None
        self.mock_result.scalar_one.return_value = 0
        self.mock_db.execute.return_value = self.mock_result

        self.repo = BaseRepository(db=self.mock_db, model=SimpleModel)

    async def test_find_many(self):
        options = RepoQueryOptions(limit=10)
        results = await self.repo.find_many(options)

        self.assertEqual(results, [])
        self.mock_db.execute.assert_called_once()

    async def test_create(self):
        instance = SimpleModel(id=uuid.uuid4(), name='Test')
        created = await self.repo.create(instance)

        self.assertEqual(created, instance)
        self.mock_db.add.assert_called_once_with(instance)
        self.mock_db.flush.assert_called_once()

    async def test_update(self):
        instance_id = uuid.uuid4()
        mock_instance = SimpleModel(id=instance_id, name='Old Name')

        # Mock finding the instance
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = mock_instance
        self.mock_db.execute.return_value = mock_result

        updated = await self.repo.update(instance_id, {'name': 'New Name'})

        self.assertEqual(updated.name, 'New Name')
        self.mock_db.flush.assert_called()

    async def test_delete_hard(self):
        # Create a model WITHOUT deleted_at for hard delete test
        class HardDeleteModel(Base):
            __tablename__ = 'hard_delete_model'
            id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)

        repo = BaseRepository(db=self.mock_db, model=HardDeleteModel)

        instance_id = uuid.uuid4()
        mock_instance = HardDeleteModel(id=instance_id)

        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = mock_instance
        self.mock_db.execute.return_value = mock_result

        success = await repo.delete(instance_id)

        self.assertTrue(success)
        self.mock_db.delete.assert_called_once_with(mock_instance)
        self.mock_db.flush.assert_called()

    async def test_delete_soft(self):
        instance_id = uuid.uuid4()
        mock_instance = SimpleModel(id=instance_id, deleted_at=None)

        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = mock_instance
        self.mock_db.execute.return_value = mock_result

        success = await self.repo.delete(instance_id)

        self.assertTrue(success)
        self.assertIsNotNone(mock_instance.deleted_at)
        self.mock_db.delete.assert_not_called()
        self.mock_db.flush.assert_called()

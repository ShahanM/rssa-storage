import unittest
import uuid
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy import Integer, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from rssa_storage.shared import BaseOrderedRepository


class Base(DeclarativeBase):
    pass


class MockOrderedModel(Base):
    __tablename__ = 'test_ordered_model'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_position: Mapped[int] = mapped_column(Integer, default=0)
    parent_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)


class TestBaseOrderedRepo(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_result = MagicMock()
        self.mock_result.scalars.return_value.all.return_value = []
        self.mock_result.scalars.return_value.first.return_value = None
        self.mock_db.execute.return_value = self.mock_result

        class ConcreteOrderedRepo(BaseOrderedRepository[MockOrderedModel]):
            parent_id_column_name = 'parent_id'

        self.repo = ConcreteOrderedRepo(db=self.mock_db, model=MockOrderedModel)

    async def test_get_all_ordered_instances(self):
        parent_id = uuid.uuid4()
        await self.repo.get_all_ordered_instances(parent_id)

        self.mock_db.execute.assert_called_once()

    async def test_delete_ordered_instance(self):
        instance_id = uuid.uuid4()
        parent_id = uuid.uuid4()
        mock_instance = MockOrderedModel(id=instance_id, parent_id=parent_id, order_position=5)

        # Mock finding the instance
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = mock_instance
        self.mock_db.execute.return_value = mock_result

        await self.repo.delete_ordered_instance(instance_id)

        self.assertTrue(self.mock_db.delete.called)
        # execute called for find_one and update
        self.assertGreaterEqual(self.mock_db.execute.call_count, 2)

    async def test_reorder_ordered_instances(self):
        parent_id = uuid.uuid4()
        instances_map = {uuid.uuid4(): 1, uuid.uuid4(): 2}

        await self.repo.reorder_ordered_instances(parent_id, instances_map)

        self.assertEqual(self.mock_db.execute.call_count, 2)
        self.mock_db.flush.assert_called_once()

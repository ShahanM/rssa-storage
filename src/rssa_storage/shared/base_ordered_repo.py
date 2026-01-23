"""Base repository for ordered models."""

import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, TypeVar

from sqlalchemy import Select, case, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseRepository, RepoQueryOptions

# from rssa_api.data.models.rssa_base_models import DBBaseOrderedModel
from .db_utils import SharedOrderedModel

# ModelType = TypeVar('ModelType', bound=DBBaseOrderedModel)
ModelType = TypeVar('ModelType', bound=SharedOrderedModel)


@dataclass
class OrderedRepoQueryOptions(RepoQueryOptions):
    """Query options for ordered repositories."""

    min_order_position: int | None = None


class BaseOrderedRepository(BaseRepository[ModelType]):
    """Base repository for ordered models."""

    parent_id_column_name: str

    def __init__(
        self,
        db: AsyncSession,
        model: type[ModelType] | None = None,
        parent_id_column_name: str | None = None,
    ):
        """Initialize the BaseOrderedRepository.

        Args:
            db: The database session.
            model: The model class.
            parent_id_column_name: The name of the parent ID column in the model.
        """
        super().__init__(db, model)

        if parent_id_column_name:
            self.parent_id_column_name = parent_id_column_name

        if not self.parent_id_column_name:
            raise ValueError(
                f"Repository '{self.__class__.__name__}' must define 'parent_id_column_name' "
                'as a class attribute or pass it to __init__.'
            )
        self.parent_id_column = getattr(self.model, self.parent_id_column_name, None)

        if self.parent_id_column is None:
            raise AttributeError(
                f"Model '{self.model.__name__}' does not have a column named '{self.parent_id_column_name}'."
            )

    def _apply_query_options(self, query: Select, options: RepoQueryOptions) -> Select:
        """Apply query options to the query.

        Args:
            query: The SQLAlchemy query.
            options: The query options.

        Returns:
            The modified query.
        """
        query = super()._apply_query_options(query, options)

        if isinstance(options, OrderedRepoQueryOptions):
            if options.min_order_position is not None:
                query = query.where(self.model.order_position > options.min_order_position)

        return query

    async def find_many(self, options: RepoQueryOptions | None = None) -> Sequence[ModelType]:
        """Find many ordered instances based on query options.

        Args:
            options: Query options including filters, sorting, pagination, etc.

        Returns:
            A list of ordered instances.
        """
        if options is None:
            options = OrderedRepoQueryOptions()

        options.sort_by = options.sort_by or 'order_position'
        options.sort_desc = options.sort_desc

        return await super().find_many(options)

    async def get_all_ordered_instances(
        self,
        parent_id: uuid.UUID,
        limit: int | None = None,
        include_deleted: bool = False,
    ) -> Sequence[ModelType]:
        """Get all ordered instances for a given parent ID.

        Args:
            parent_id: The parent ID.
            limit: Optional limit on the number of instances to retrieve.
            include_deleted: Whether to include soft-deleted instances.

        Returns:
            A list of ordered instances.
        """
        options = OrderedRepoQueryOptions(
            filters={self.parent_id_column_name: parent_id},
            sort_by='order_position',
            sort_desc=False,
            limit=limit,
            include_deleted=include_deleted,
        )
        return await self.find_many(options)

    async def get_first_ordered_instance(
        self,
        parent_id: uuid.UUID,
        load_options: Sequence[Any] | None = None,
    ) -> ModelType | None:
        """Get the first ordered instance for a given parent ID.

        Args:
            parent_id: The parent ID.
            load_options: Optional list of loading options.

        Returns:
            The first ordered instance or None if not found.
        """
        options = OrderedRepoQueryOptions(
            filters={self.parent_id_column_name: parent_id},
            sort_by='order_position',
            sort_desc=False,
            limit=1,
            load_options=load_options,
        )
        return await self.find_one(options)

    async def get_next_ordered_instance(self, current_instance: ModelType) -> ModelType | None:
        """Get the next ordered instance after the current instance.

        Args:
            current_instance: The current ordered instance.

        Returns:
            The next ordered instance or None if not found.
        """
        parent_id = getattr(current_instance, self.parent_id_column_name)

        options = OrderedRepoQueryOptions(
            filters={self.parent_id_column_name: parent_id},
            min_order_position=current_instance.order_position,
            sort_by='order_position',
            sort_desc=False,
            limit=1,
        )
        return await self.find_one(options)

    async def get_last_ordered_instance(self, parent_id: uuid.UUID) -> ModelType | None:
        """Get the last ordered instance for a given parent ID.

        Args:
            parent_id: The parent ID.

        Returns:
            The last ordered instance or None if not found.
        """
        options = RepoQueryOptions(
            filters={self.parent_id_column_name: parent_id},
            sort_by='order_position',
            sort_desc=True,
            limit=1,
            include_deleted=True,
        )
        return await self.find_one(options)

    async def delete_ordered_instance(self, instance_id: uuid.UUID) -> None:
        """Delete ordered instance and update order positions of subsequent instances.

        Args:
            instance_id: The ID of the instance to delete.

        Returns:
            None
        """
        # instance = await self.get(instance_id)
        instance = await self.find_one(RepoQueryOptions(filters={'id': instance_id}))

        if instance:
            deleted_position = instance.order_position
            parent_id = getattr(instance, self.parent_id_column_name)

            await self.delete(instance_id)

            update_stmt = (
                update(self.model)
                .where(self.parent_id_column == parent_id, self.model.order_position > deleted_position)
                .values(order_position=self.model.order_position - 1)
            )

            await self.db.execute(update_stmt)
            await self.db.flush()

    async def purge_ordered_instance(self, instance_id: uuid.UUID) -> None:
        """Purge ordered instance from the database (non-reversible).

        Args:
            instance_id: The ID of the instance to purge.

        Returns:
            None
        """
        # instance = await self.get(instance_id)
        instance = await self.find_one(RepoQueryOptions(filters={'id': instance_id}))

        if instance:
            deleted_position = instance.order_position
            parent_id = getattr(instance, self.parent_id_column_name)

            await self.db.delete(instance)

            update_stmt = (
                update(self.model)
                .where(self.parent_id_column == parent_id, self.model.order_position > deleted_position)
                .values(order_position=self.model.order_position - 1)
            )

            await self.db.execute(update_stmt)
            await self.db.flush()

    async def reorder_ordered_instances(self, parent_id: uuid.UUID, instances_map: dict[uuid.UUID, int]) -> None:
        """Reorder ordered instances based on the provided mapping.

        Args:
            parent_id: The parent ID.
            instances_map: A mapping of instance IDs to their new order positions.

        Returns:
            None
        """
        if not instances_map:
            return

        # Ghost Eviction: Move soft-deleted items out of the target positions
        target_positions = list(instances_map.values())

        # Check if model has soft delete support
        if hasattr(self.model, 'deleted_at'):
            # Find ghosts in the way
            ghost_query = select(self.model.id, self.model.order_position).where(
                getattr(self.model, self.parent_id_column_name) == parent_id,
                self.model.deleted_at.is_not(None),
                self.model.order_position.in_(target_positions),
            )
            ghosts = await self.db.execute(ghost_query)
            ghost_ids = [row.id for row in ghosts]

            if ghost_ids:
                # Evict them to a safe range (e.g., current + 1,000,000)
                # We use a simple shift to avoid collisions among ghosts themselves
                evict_stmt = (
                    update(self.model)
                    .where(self.model.id.in_(ghost_ids))
                    .values(order_position=self.model.order_position + 1000000)
                )
                await self.db.execute(evict_stmt)

        # Negative Intermediate Update: Move to negative target positions
        # This avoids collisions with existing positive values and other items being swapped.

        # Step A: Update to negative values (e.g. 2 -> -2)
        whens = [(self.model.id == uid, -1 * pos) for uid, pos in instances_map.items()]

        stmt_neg = (
            update(self.model)
            .where(
                getattr(self.model, self.parent_id_column_name) == parent_id, self.model.id.in_(instances_map.keys())
            )
            .values(order_position=case(*whens))
        )

        await self.db.execute(stmt_neg)

        # Step B: Flip back to positive values
        # We target the specific IDs to be safe, though parent_id filter would also work finding negatives.
        stmt_pos = (
            update(self.model)
            .where(
                getattr(self.model, self.parent_id_column_name) == parent_id, self.model.id.in_(instances_map.keys())
            )
            .values(order_position=func.abs(self.model.order_position))
        )

        await self.db.execute(stmt_pos)
        await self.db.flush()

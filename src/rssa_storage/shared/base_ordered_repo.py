"""Base repository for ordered models."""

import uuid
from collections.abc import Sequence
from typing import TypeVar, cast

from sqlalchemy import case, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseRepository
from .db_utils import SharedOrderedModel
from .repo_utils import OrderedRepoQueryOptions, RepoQueryOptions, merge_repo_query_options

ModelType = TypeVar('ModelType', bound=SharedOrderedModel)


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

    async def find_many(self, options: RepoQueryOptions | None = None) -> Sequence[ModelType]:
        """Find many ordered instances based on query options."""
        if options is None:
            options = OrderedRepoQueryOptions()

        options.sort_by = options.sort_by or 'order_position'
        options.sort_desc = options.sort_desc

        return await super().find_many(options)

    def _apply_ordered_options(
        self, parent_id: uuid.UUID, options: OrderedRepoQueryOptions | None = None
    ) -> OrderedRepoQueryOptions:
        _options = OrderedRepoQueryOptions(filters={self.parent_id_column_name: parent_id})
        if options is not None:
            _options = cast(OrderedRepoQueryOptions, merge_repo_query_options(_options, options))
        _options.sort_by = 'order_position'
        _options.sort_desc = False
        _options.limit = 1

        return _options

    async def get_first_ordered_instance(
        self,
        parent_id: uuid.UUID,
        options: OrderedRepoQueryOptions | None = None,
    ) -> ModelType | None:
        """Get the first ordered instance for a given parent ID."""

        return await self.find_one(self._apply_ordered_options(parent_id, options))

    async def get_next_ordered_instance(
        self, current_instance: ModelType, options: OrderedRepoQueryOptions | None = None
    ) -> ModelType | None:
        """Get the next ordered instance after the current instance.

        Args:
            current_instance: The current ordered instance.

        Returns:
            The next ordered instance or None if not found.
        """
        parent_id = getattr(current_instance, self.parent_id_column_name)

        return await self.find_one(self._apply_ordered_options(parent_id, options))

    async def get_last_ordered_instance(
        self, parent_id: uuid.UUID, options: OrderedRepoQueryOptions
    ) -> ModelType | None:
        """Get the last ordered instance for a given parent ID."""
        return await self.find_one(self._apply_ordered_options(parent_id, options))

    async def delete_ordered_instance(self, instance_id: uuid.UUID) -> None:
        """Delete ordered instance and update order positions of subsequent instances.

        Args:
            instance_id: The ID of the instance to delete.

        Returns:
            None
        """
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
        instance = await self.find_one(RepoQueryOptions(filters={'id': instance_id}, include_deleted=True))

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

        target_positions = list(instances_map.values())

        if hasattr(self.model, 'deleted_at'):
            ghost_query = select(self.model.id, self.model.order_position).where(
                getattr(self.model, self.parent_id_column_name) == parent_id,
                self.model.deleted_at.is_not(None),  # type: ignore
                self.model.order_position.in_(target_positions),
            )
            ghosts = await self.db.execute(ghost_query)
            ghost_ids = [row.id for row in ghosts]

            if ghost_ids:
                evict_stmt = (
                    update(self.model)
                    .where(self.model.id.in_(ghost_ids))
                    .values(order_position=self.model.order_position + 1000000)
                )
                await self.db.execute(evict_stmt)

        whens = [(self.model.id == uid, -1 * pos) for uid, pos in instances_map.items()]

        stmt_neg = (
            update(self.model)
            .where(
                getattr(self.model, self.parent_id_column_name) == parent_id, self.model.id.in_(instances_map.keys())
            )
            .values(order_position=case(*whens))
        )

        await self.db.execute(stmt_neg)

        stmt_pos = (
            update(self.model)
            .where(
                getattr(self.model, self.parent_id_column_name) == parent_id, self.model.id.in_(instances_map.keys())
            )
            .values(order_position=func.abs(self.model.order_position))
        )

        await self.db.execute(stmt_pos)
        await self.db.flush()

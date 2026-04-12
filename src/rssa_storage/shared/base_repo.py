"""Base repository providing generic CRUD operations for SQLAlchemy models."""

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Generic, Protocol, TypeGuard, TypeVar, get_args

from sqlalchemy import Select, UniqueConstraint, and_, func, inspect, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, load_only, selectinload, with_loader_criteria
from sqlalchemy.sql.base import ExecutableOption

from rssa_storage.shared.db_utils import SharedModel, SoftDeleteMixin

T = TypeVar('T', bound=SharedModel)


@dataclass
class RepoQueryOptions:
    """Data class to encapsulate common query options for repositories."""

    ids: list[uuid.UUID] | None = None
    filters: dict[str, Any] = field(default_factory=dict)
    filter_ranges: list[tuple[str, str, Any]] = field(default_factory=list)
    filter_ilike: dict[str, str] = field(default_factory=dict)
    filter_not_null: list[str] = field(default_factory=list)
    search_text: str | None = None
    search_columns: list[str] = field(default_factory=list)
    sort_by: str | None = None
    sort_desc: bool = False
    limit: int | None = None
    offset: int | None = None
    include_deleted: bool = False
    load_options: Sequence[ExecutableOption] | None = field(default_factory=list)
    load_columns: list[str] | None = None
    load_relationships: dict[str, Any] | None = field(default_factory=dict)


class SoftDeletable(Protocol):
    """A protocol for models that can be soft-deleted."""

    deleted_at: Any


def is_soft_deletable(instance: Any) -> TypeGuard[SoftDeletable]:
    """A type guard to check if an instance can be soft-deleted."""
    return hasattr(instance, 'deleted_at')


class BaseRepository(Generic[T]):
    """Base repository providing generic CRUD operations for SQLAlchemy models.

    Attributes:
        db (AsyncSession): The asynchronous database session.
        model (Type[T]): The SQLAlchemy model class.
    """

    def __init__(self, db: AsyncSession, model: type[T] | None = None):
        """Initialize the BaseRepository.

        Args:
            db: The asynchronous database session.
            model: The SQLAlchemy model class.
        """
        self.db = db

        if model:
            self.model = model
        else:
            inferred_model = self._infer_model_type()
            if inferred_model is None:
                raise ValueError(
                    f'Could not automatically infer T for {self.__class__.__name__}. '
                    "Please pass the 'model' argument explicitly."
                )
            self.model = inferred_model

    def _infer_model_type(self) -> type[T] | None:
        """Inspects the class hierarchy to find the generic type argument for T."""
        cls = self.__class__
        for base in cls.__orig_bases__:  # type: ignore[attr-defined]
            origin = getattr(base, '__origin__', None)

            if origin is BaseRepository or (origin and issubclass(origin, BaseRepository)):
                args = get_args(base)

                if args and len(args) > 0:
                    return args[0]
        return None

    def _apply_query_options(self, query: Select, options: RepoQueryOptions) -> Select:
        """Centralized method to apply common query options to a SQLAlchemy Select query."""
        query = self._apply_filtering_to_query(query, options)
        query = self._apply_sorting_and_pagination(query, options)
        query = self._apply_load_options(query, options)

        if not options.include_deleted:
            query = self._apply_soft_delete_criteria(query)

        return query

    def _apply_sorting_and_pagination(self, query: Select, options: RepoQueryOptions) -> Select:
        """Apply sorting, limit, and offset mutations to the query."""
        if options.sort_by:
            query = self._sort(query, options.sort_by, options.sort_desc)

        if options.limit:
            query = query.limit(options.limit)

        if options.offset:
            query = query.offset(options.offset)

        return query

    def _build_column_loaders(self, load_columns: list[str]) -> list[ExecutableOption]:
        """Build deferred loading options (load_only) for top-level columns."""
        column_attrs = []
        for col_name in load_columns:
            attr = getattr(self.model, col_name, None)
            if isinstance(attr, InstrumentedAttribute) and hasattr(attr.property, 'columns'):
                column_attrs.append(attr)

        return [load_only(*column_attrs)] if column_attrs else []

    def _build_relationship_loaders(
        self, model_class: type, rel_dict: dict[str, Any], current_path: Any = None
    ) -> list[ExecutableOption]:
        """Recursively build eager load strategies (selectinload) for relationships."""
        loaders = []

        for rel_name, rel_data in rel_dict.items():
            rel_attr = getattr(model_class, rel_name, None)

            if isinstance(rel_attr, InstrumentedAttribute) and hasattr(rel_attr.property, 'mapper'):
                loader = selectinload(rel_attr) if current_path is None else current_path.selectinload(rel_attr)

                rel_columns = rel_data.get('columns', [])
                nested_rels = rel_data.get('relationships', {})
                nested_model = rel_attr.property.mapper.class_

                if rel_columns:
                    nested_attrs = []
                    for col_name in rel_columns:
                        child_attr = getattr(nested_model, col_name, None)
                        if isinstance(child_attr, InstrumentedAttribute) and hasattr(child_attr.property, 'columns'):
                            nested_attrs.append(child_attr)
                    if nested_attrs:
                        loader = loader.load_only(*nested_attrs)

                loaders.append(loader)

                if nested_rels:
                    loaders.extend(self._build_relationship_loaders(nested_model, nested_rels, loader))

        return loaders

    def _apply_load_options(self, query: Select, options: RepoQueryOptions) -> Select:
        """Apply deferred column loading and relationship eager loading strategies."""
        if options.load_options:
            query = query.options(*options.load_options)

        if options.load_columns:
            col_loaders = self._build_column_loaders(options.load_columns)
            if col_loaders:
                query = query.options(*col_loaders)

        if options.load_relationships:
            rel_loaders = self._build_relationship_loaders(self.model, options.load_relationships)
            if rel_loaders:
                query = query.options(*rel_loaders)

        return query

    def _apply_filtering_to_query(self, query: Select, options: RepoQueryOptions) -> Select:
        """Apply filtering options (filters, ranges, search, etc.) to the query."""
        if options.ids:
            query = query.where(self.model.id.in_(options.ids))

        if options.filters:
            query = self._filter(query, options.filters)

        if options.filter_ranges:
            query = self._apply_range_filters(query, options.filter_ranges)

        if options.filter_ilike:
            query = self._apply_ilike_filters(query, options.filter_ilike)

        if options.filter_not_null:
            query = self._apply_not_null_filters(query, options.filter_not_null)

        if options.search_text and options.search_columns:
            query = self._filter_similar(query, options.search_text, options.search_columns)

        return query

    def _apply_range_filters(self, query: Select, ranges: list[tuple[str, str, Any]]) -> Select:
        """Apply range filters (>=, <=) to the query.

        Args:
            query: The SQLAlchemy Select query.
            ranges: List of tuples (column_name, operator, value).
                    Operator can be '>=', '<=', '>', '<'.
        """
        for col_name, op, value in ranges:
            col_attr = getattr(self.model, col_name, None)
            if col_attr is not None:
                if op == '>=':
                    query = query.where(col_attr >= value)
                elif op == '<=':
                    query = query.where(col_attr <= value)
                elif op == '>':
                    query = query.where(col_attr > value)
                elif op == '<':
                    query = query.where(col_attr < value)
        return query

    def _apply_not_null_filters(self, query: Select, columns: list[str]) -> Select:
        """Apply IS NOT NULL filters to specific columns or relationships.

        Args:
            query: The SQLAlchemy Select query.
            columns: List of column/relationship names to check for existence (NOT NULL).
        """
        mapper = inspect(self.model)

        for col_name in columns:
            col_attr = getattr(self.model, col_name, None)
            if col_attr is not None:
                if col_name in mapper.relationships:
                    relationship = mapper.relationships[col_name]
                    if relationship.uselist:
                        query = query.where(col_attr.any())
                    else:
                        query = query.where(col_attr.has())
                else:
                    query = query.where(col_attr.is_not(None))
        return query

    def _apply_ilike_filters(self, query: Select, filters: dict[str, str]) -> Select:
        """Apply ILIKE filters to specific columns.

        Args:
            query: The SQLAlchemy Select query.
            filters: Dictionary of {column_name: search_string}.
        """
        for col_name, value in filters.items():
            col_attr = getattr(self.model, col_name, None)
            if col_attr is not None:
                query = query.where(col_attr.ilike(f'%{value}%'))
        return query

    def _apply_soft_delete_filter(self, query: Select) -> Select:
        """Modify the query to exclude soft-deleted records.

        Args:
            query: The SQLAlchemy Select query to modify.

        Returns:
            The modified Select query excluding soft-deleted records.
        """
        deleted_attr = getattr(self.model, 'deleted_at', None)
        if deleted_attr is not None:
            query = query.where(deleted_attr.is_(None))
        return query

    def _apply_soft_delete_criteria(self, query: Select) -> Select:
        """Apply soft delete filters to the main model and all loaded relationships."""
        query = self._apply_soft_delete_filter(query)

        query = query.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )
        return query

    async def find_many(self, options: RepoQueryOptions | None = None) -> Sequence[T]:
        """Find multiple instances based on the provided query options.

        Args:
            options: The query options to apply.

        Returns:
            A list of instances matching the query options.
        """
        options = options or RepoQueryOptions()
        query = select(self.model)
        query = self._apply_query_options(query, options)
        result = await self.db.execute(query)

        return result.scalars().all()

    async def find_one(self, options: RepoQueryOptions | None = None) -> T | None:
        """Find a single instance based on the provided query options.

        Args:
            options: The query options to apply.

        Returns:
            An instance matching the query options, or None if not found.
        """
        options = options or RepoQueryOptions()
        query = select(self.model)
        query = self._apply_query_options(query, options)
        query = query.limit(1)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_existing_by_unique_fields(self, instance: T) -> T | None:
        """Dynamically find an existing record that matches the unique constraints of the instance."""
        mapper = inspect(self.model)
        unique_conditions = []

        for column in mapper.attrs:
            if hasattr(column, 'columns') and column.columns[0].unique:
                val = getattr(instance, column.key)
                if val is not None:
                    unique_conditions.append(getattr(self.model, column.key) == val)

        for constraint in getattr(self.model.__table__, 'constraints', []):
            if isinstance(constraint, UniqueConstraint):
                col_conditions = []
                has_null = False

                for col in constraint.columns:
                    val = getattr(instance, col.name)
                    if val is None:
                        has_null = True
                        break
                    col_conditions.append(getattr(self.model, col.name) == val)
                if not has_null and col_conditions:
                    unique_conditions.append(and_(*col_conditions))

        if not unique_conditions:
            return None

        query = select(self.model).where(or_(*unique_conditions))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, instance: T) -> T:
        """Create a new instance in the database.

        Args:
            instance: The instance to create.

        Returns:
            The created instance.
        """
        try:
            self.db.add(instance)
            await self.db.flush()
            return instance
        except Exception as e:
            await self.db.rollback()

            if isinstance(e, IntegrityError):
                existing = await self.find_existing_by_unique_fields(instance)
                if existing:
                    return existing
            raise e

    async def create_all(self, instances: list[T]) -> list[T]:
        """Create multiple instances in the database.

        Args:
            instances: A list of instances to create.

        Returns:
            The list of created instances.
        """
        self.db.add_all(instances)
        await self.db.flush()
        return instances

    async def update(self, instance_id: uuid.UUID, updated_fields: dict[str, Any]) -> T | None:
        """Update an instance in the database.

        Args:
            instance_id: The ID of the instance to update.
            updated_fields: A dictionary of fields to update.

        Returns:
            The updated instance or None if not found.
        """
        instance = await self.find_one(RepoQueryOptions(ids=[instance_id]))
        if instance:
            for field_name, value in updated_fields.items():
                setattr(instance, field_name, value)
            await self.db.flush()
            return instance
        return None

    async def delete(self, instance_id: uuid.UUID) -> bool:
        """Delete an instance from the database.

        Args:
            instance_id: The ID of the instance to delete.

        Returns:
            True if the instance was deleted, False otherwise.
        """
        instance = await self.find_one(RepoQueryOptions(ids=[instance_id]))
        if instance:
            if is_soft_deletable(instance):
                from datetime import UTC, datetime

                instance.deleted_at = datetime.now(UTC)
            else:
                await self.db.delete(instance)
            await self.db.flush()
            return True
        return False

    async def batch_update(self, update_data: Sequence[dict[str, Any]]) -> bool:
        """Update multiple instances in a single batch operation.

        Args:
            update_data: A list of dictionaries. Each dictionary MUST contain
                        the primary key field (e.g., 'id') to identify the
                        target record, along with the specific fields to update.

        Returns:
            True if the batch update executed successfully, False if no data was provided.
        """
        if not update_data:
            return False

        try:
            # SQLAlchemy 2.0 bulk update: pass the update construct and the list of mappings
            await self.db.execute(update(self.model), update_data)
            await self.db.flush()
            return True
        except Exception as e:
            await self.db.rollback()
            raise e

    def _filter_similar(
        self, query: Select, filter_str: str | None = None, filter_cols: list[str] | None = None
    ) -> Select:
        """Add search filters to the query based on specified columns.

        Args:
            query: The SQLAlchemy Select query to modify.
            filter_str: The search string to filter by.
            filter_cols: A list of column names to apply the search filter on.

        Returns:
            The modified Select query with search filters applied.
        """
        if filter_str and filter_cols:
            search_pattern = f'%{filter_str}%'
            conditions = []
            for col_name in filter_cols:
                column_attribute = getattr(self.model, col_name)
                conditions.append(column_attribute.ilike(search_pattern))
            return query.where(or_(*conditions))

        return query

    def _filter(self, query: Select, filters: dict[str, Any]) -> Select:
        """Add exact match filters to the query based on specified columns.

        Args:
            query: The SQLAlchemy Select query to modify.
            filters: A list of tuples where each tuple contains a field name and its corresponding value.

        Returns:
            The modified Select query with exact match filters applied.
        """
        for col_name, col_val in filters.items():
            col_attr = getattr(self.model, col_name)
            if col_attr is not None:
                if isinstance(col_val, (list, tuple)):
                    query = query.where(col_attr.in_(col_val))
                else:
                    query = query.where(col_attr == col_val)

        return query

    def _sort(self, query: Select, sort_by: str, desc: bool = False) -> Select:
        """Sort the query by a specified column and direction.

        Args:
            query: The SQLAlchemy Select query to modify.
            sort_by: The column name to sort by.
            sort_dir: The direction of sorting ('asc' or 'desc').

        Returns:
            The modified Select query with sorting applied.
        """
        col_to_sort = getattr(self.model, sort_by, None)
        if col_to_sort is not None:
            if desc:
                query = query.order_by(col_to_sort.desc())
            else:
                query = query.order_by(col_to_sort.asc())
        return query

    async def count(self, options: RepoQueryOptions) -> int:
        """Count the total number of instances of the model.

        Returns:
            The total number of instances.
        """
        query = select(func.count()).select_from(self.model)
        if not options.include_deleted:
            query = self._apply_soft_delete_criteria(query)
        query = self._apply_filtering_to_query(query, options)

        result = await self.db.execute(query)
        return result.scalar_one()

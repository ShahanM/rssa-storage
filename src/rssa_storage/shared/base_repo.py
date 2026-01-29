"""Base repository providing generic CRUD operations for SQLAlchemy models."""

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Generic, Protocol, TypeGuard, TypeVar, get_args

from sqlalchemy import Select, UniqueConstraint, and_, func, inspect, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from rssa_storage.shared.db_utils import SharedModel

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


def merge_repo_query_options(options1: RepoQueryOptions, options2: RepoQueryOptions) -> RepoQueryOptions:
    """Merge two RepoQueryOptions objects.

    Merge strategy:
    - Lists/Sequences: Concatenated (ids, filter_ranges, filter_not_null, search_columns, load_options)
    - Dictionaries: Merged, with options2 overriding options1 (filters, filter_ilike)
    - Scalars: options2 overrides options1 if explicit value provided (not None/default), else options1
    """
    merged = RepoQueryOptions()

    # Merge IDs: Concatenate if any are present.
    if options1.ids is not None or options2.ids is not None:
        merged.ids = (options1.ids or []) + (options2.ids or [])

    # Merge dictionaries
    merged.filters = {**options1.filters, **options2.filters}
    merged.filter_ilike = {**options1.filter_ilike, **options2.filter_ilike}

    # Merge lists (concatenation)
    merged.filter_ranges = options1.filter_ranges + options2.filter_ranges
    merged.filter_not_null = list(set(options1.filter_not_null + options2.filter_not_null))
    merged.search_columns = list(set(options1.search_columns + options2.search_columns))

    # For load_options, we want to combine them
    opt1_load = list(options1.load_options) if options1.load_options else []
    opt2_load = list(options2.load_options) if options2.load_options else []
    merged.load_options = tuple(opt1_load + opt2_load)

    # Scalars - options2 takes precedence if set (not None)
    merged.search_text = options2.search_text if options2.search_text is not None else options1.search_text
    merged.limit = options2.limit if options2.limit is not None else options1.limit
    merged.offset = options2.offset if options2.offset is not None else options1.offset

    # Sort behavior: if options2 specifies sort_by, it dictates the sort.
    if options2.sort_by:
        merged.sort_by = options2.sort_by
        merged.sort_desc = options2.sort_desc
    else:
        merged.sort_by = options1.sort_by
        merged.sort_desc = options1.sort_desc

    # If anyone wants deleted included, it should be included.
    merged.include_deleted = options1.include_deleted or options2.include_deleted

    return merged


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

        if options.sort_by:
            query = self._sort(query, options.sort_by, options.sort_desc)

        if options.limit:
            query = query.limit(options.limit)

        if options.offset:
            query = query.offset(options.offset)

        if options.load_options:
            query = query.options(*options.load_options)

        if not options.include_deleted:
            query = self._apply_soft_delete(query)

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

    def _apply_soft_delete(self, query: Select) -> Select:
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
                # if hasattr(instance, 'deleted_at'):
                from datetime import UTC, datetime

                instance.deleted_at = datetime.now(UTC)
            else:
                await self.db.delete(instance)
            await self.db.flush()
            return True
        return False

    def _filter_similar(
        self,
        query: Select,
        filter_str: str | None = None,
        filter_cols: list[str] | None = None,
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

    def _filter(
        self,
        query: Select,
        filters: dict[str, Any],
    ) -> Select:
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

    async def count(
        self,
        filter_str: str | None = None,
        filter_cols: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        include_deleted: bool = False,
        filter_ranges: list[tuple[str, str, Any]] | None = None,
        filter_ilike: dict[str, str] | None = None,
        filter_not_null: list[str] | None = None,
    ) -> int:
        """Count the total number of instances of the model.

        Returns:
            The total number of instances.
        """
        query = select(func.count()).select_from(self.model)
        if not include_deleted:
            query = self._apply_soft_delete(query)
        query = self._filter_similar(query, filter_str, filter_cols)
        query = self._filter(query, filters or {})

        if filter_ranges:
            query = self._apply_range_filters(query, filter_ranges)

        if filter_ilike:
            query = self._apply_ilike_filters(query, filter_ilike)

        if filter_not_null:
            query = self._apply_not_null_filters(query, filter_not_null)

        result = await self.db.execute(query)
        return result.scalar_one()

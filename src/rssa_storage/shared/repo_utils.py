import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy.sql.base import ExecutableOption


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


@dataclass
class OrderedRepoQueryOptions(RepoQueryOptions):
    """Query options for ordered repositories."""

    min_order_position: int | None = None


QueryUnionType = RepoQueryOptions | OrderedRepoQueryOptions


def merge_repo_query_options(options1: RepoQueryOptions, options2: RepoQueryOptions) -> QueryUnionType:
    """Merge two RepoQueryOptions objects.

    Merge strategy:
    - Lists/Sequences: Concatenated (ids, filter_ranges, filter_not_null, search_columns, load_options)
    - Dictionaries: Merged, with options2 overriding options1 (filters, filter_ilike)
    - Scalars: options2 overrides options1 if explicit value provided (not None/default), else options1
    """
    is_ordered_1 = isinstance(options1, OrderedRepoQueryOptions)
    is_ordered_2 = isinstance(options2, OrderedRepoQueryOptions)

    if is_ordered_1 or is_ordered_2:
        merged = OrderedRepoQueryOptions()

        pos1 = getattr(options1, 'min_order_position', None) if is_ordered_1 else None
        pos2 = getattr(options2, 'min_order_position', None) if is_ordered_2 else None

        valid_positions = [p for p in (pos1, pos2) if p is not None]
        merged.min_order_position = min(valid_positions) if valid_positions else None
    else:
        merged = RepoQueryOptions()

    if options1.ids is not None or options2.ids is not None:
        merged.ids = (options1.ids or []) + (options2.ids or [])

    merged.filters = {**options1.filters, **options2.filters}
    merged.filter_ilike = {**options1.filter_ilike, **options2.filter_ilike}

    merged.filter_ranges = options1.filter_ranges + options2.filter_ranges
    merged.filter_not_null = list(set(options1.filter_not_null + options2.filter_not_null))
    merged.search_columns = list(set(options1.search_columns + options2.search_columns))

    opt1_load = list(options1.load_options) if options1.load_options else []
    opt2_load = list(options2.load_options) if options2.load_options else []
    merged.load_options = tuple(opt1_load + opt2_load)

    merged.search_text = options2.search_text if options2.search_text is not None else options1.search_text
    merged.limit = options2.limit if options2.limit is not None else options1.limit
    merged.offset = options2.offset if options2.offset is not None else options1.offset

    if options2.sort_by:
        merged.sort_by = options2.sort_by
        merged.sort_desc = options2.sort_desc
    else:
        merged.sort_by = options1.sort_by
        merged.sort_desc = options1.sort_desc

    merged.include_deleted = options1.include_deleted or options2.include_deleted

    opt1_load_cols = list(options1.load_columns) if options1.load_columns else []
    opt2_load_cols = list(options2.load_columns) if options2.load_columns else []
    merged_load_cols = list(set(opt1_load_cols + opt2_load_cols))
    merged.load_columns = merged_load_cols if len(merged_load_cols) > 0 else None

    def _merge_rels(rels1: dict, rels2: dict) -> dict:
        merged = {}
        all_keys = set(rels1.keys()).union(rels2.keys())
        for k in all_keys:
            r1 = rels1.get(k) or {}
            r2 = rels2.get(k) or {}

            c1 = r1.get('columns', [])
            c2 = r2.get('columns', [])
            n1 = r1.get('relationships', {})
            n2 = r2.get('relationships', {})

            merged[k] = {'columns': list(set(c1 + c2)), 'relationships': _merge_rels(n1, n2)}
        return merged

    opt1_rels = options1.load_relationships or {}
    opt2_rels = options2.load_relationships or {}
    merged.load_relationships = _merge_rels(opt1_rels, opt2_rels) or None

    return merged

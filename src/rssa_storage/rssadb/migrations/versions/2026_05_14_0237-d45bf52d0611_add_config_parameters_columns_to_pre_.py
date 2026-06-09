"""add config parameters columns to pre_shuffled_movie_lists

Revision ID: d45bf52d0611
Revises: 744879545586
Create Date: 2026-05-14 02:37:41.055345

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'd45bf52d0611'
down_revision: str | None = '744879545586'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('pre_shuffled_movie_lists', sa.Column('strategy', sa.String(length=100), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('year_min', sa.Integer(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('year_max', sa.Integer(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('genre', sa.String(length=100), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('min_rate_count', sa.Integer(), nullable=True))
    op.add_column(
        'pre_shuffled_movie_lists',
        sa.Column('exclude_no_emotions', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
    )
    op.add_column(
        'pre_shuffled_movie_lists',
        sa.Column('exclude_no_recommendations', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
    )
    op.add_column('pre_shuffled_movie_lists', sa.Column('page_size', sa.Integer(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('temporal_discounting', sa.Boolean(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('base_year', sa.Integer(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('decay_rate', sa.Float(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('include_genre_in_stratification', sa.Boolean(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('popular_threshold', sa.Float(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('popular_per_page', sa.Float(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('popular_growth_rate', sa.Float(), nullable=True))
    op.add_column(
        'pre_shuffled_movie_lists', sa.Column('initial_popular_schedue', sa.ARRAY(sa.Integer()), nullable=True)
    )
    op.add_column('pre_shuffled_movie_lists', sa.Column('genre_bucket_size', sa.Integer(), nullable=True))
    op.add_column('pre_shuffled_movie_lists', sa.Column('genre_repr_per_page', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('pre_shuffled_movie_lists', 'genre_repr_per_page')
    op.drop_column('pre_shuffled_movie_lists', 'genre_bucket_size')
    op.drop_column('pre_shuffled_movie_lists', 'initial_popular_schedue')
    op.drop_column('pre_shuffled_movie_lists', 'popular_growth_rate')
    op.drop_column('pre_shuffled_movie_lists', 'popular_per_page')
    op.drop_column('pre_shuffled_movie_lists', 'popular_threshold')
    op.drop_column('pre_shuffled_movie_lists', 'include_genre_in_stratification')
    op.drop_column('pre_shuffled_movie_lists', 'decay_rate')
    op.drop_column('pre_shuffled_movie_lists', 'base_year')
    op.drop_column('pre_shuffled_movie_lists', 'temporal_discounting')
    op.drop_column('pre_shuffled_movie_lists', 'page_size')
    op.drop_column('pre_shuffled_movie_lists', 'exclude_no_recommendations')
    op.drop_column('pre_shuffled_movie_lists', 'exclude_no_emotions')
    op.drop_column('pre_shuffled_movie_lists', 'min_rate_count')
    op.drop_column('pre_shuffled_movie_lists', 'genre')
    op.drop_column('pre_shuffled_movie_lists', 'year_max')
    op.drop_column('pre_shuffled_movie_lists', 'year_min')
    op.drop_column('pre_shuffled_movie_lists', 'strategy')

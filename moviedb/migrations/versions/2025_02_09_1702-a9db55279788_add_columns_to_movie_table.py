"""add columns to movie table

Revision ID: a9db55279788
Revises: f1e1ba3b9148
Create Date: 2025-02-09 17:02:06.204128

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9db55279788'
down_revision: Union[str, None] = 'f1e1ba3b9148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movies', sa.Column('imdb_genres', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('tmdb_genres', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('imdb_avg_rating', sa.Numeric(), nullable=True))
    op.add_column('movies', sa.Column('imdb_rate_count', sa.Integer(), nullable=True))
    op.add_column('movies', sa.Column('tmdb_avg_rating', sa.Numeric(), nullable=True))
    op.add_column('movies', sa.Column('tmdb_rate_count', sa.Integer(), nullable=True))
    op.add_column('movies', sa.Column('movielens_avg_rating', sa.Numeric(), nullable=True))
    op.add_column('movies', sa.Column('movielens_rate_count', sa.Integer(), nullable=True))
    op.add_column('movies', sa.Column('origin_country', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('parental_guide', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('movie_lens_dataset', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.add_column('movies', sa.Column('tmdb_poster', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('movies', 'tmdb_poster')
    op.drop_column('movies', 'last_updated')
    op.drop_column('movies', 'movie_lens_dataset')
    op.drop_column('movies', 'parental_guide')
    op.drop_column('movies', 'origin_country')
    op.drop_column('movies', 'movielens_rate_count')
    op.drop_column('movies', 'movielens_avg_rating')
    op.drop_column('movies', 'tmdb_rate_count')
    op.drop_column('movies', 'tmdb_avg_rating')
    op.drop_column('movies', 'imdb_rate_count')
    op.drop_column('movies', 'imdb_avg_rating')
    op.drop_column('movies', 'tmdb_genres')
    op.drop_column('movies', 'imdb_genres')

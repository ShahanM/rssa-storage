"""create movies table

Revision ID: a5acb0321e2e
Revises: 
Create Date: 2024-10-11 02:10:12.035988

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5acb0321e2e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'movies',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('movielens_id', sa.String, nullable=False),
        sa.Column('tmdb_id', sa.String, nullable=True),
        sa.Column('imdb_id', sa.String, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('year', sa.Integer, nullable=False),
        sa.Column('runtime', sa.Integer, nullable=False),
        sa.Column('genre', sa.String, nullable=False),
        sa.Column('ave_rating', sa.Numeric, nullable=False),
        sa.Column('director', sa.Text, nullable=False),
        sa.Column('writer', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('cast', sa.Text, nullable=False),
        sa.Column('poster', sa.String, nullable=False),
        sa.Column('count', sa.Integer, nullable=False),
        sa.Column('rank', sa.Integer, nullable=False),
        sa.Column('poster_identifier', sa.String, nullable=False)
    )

    op.create_index('movielens_id_idx', 'movies', ['movielens_id'], unique=True)
    op.create_index('imdb_id_idx', 'movies', ['imdb_id'], unique=True)


def downgrade() -> None:
    op.drop_index('movielens_id_idx')
    op.drop_index('imdb_id_idx')
    op.drop_table('movies')


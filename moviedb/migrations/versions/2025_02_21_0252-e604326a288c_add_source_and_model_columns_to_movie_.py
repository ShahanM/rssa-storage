"""add source and model columns to movie_recommendation_text

Revision ID: e604326a288c
Revises: 57ad9df93d10
Create Date: 2025-02-21 02:52:55.560724

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e604326a288c'
down_revision: Union[str, None] = '57ad9df93d10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movie_recommendation_text', sa.Column('source', sa.String(), nullable=True))
    op.add_column('movie_recommendation_text', sa.Column('model', sa.String(), nullable=True))

    # Make the movie_id column indexed
    op.create_index('ix_movie_recommendation_text_movie_id', 'movie_recommendation_text', ['movie_id'])


def downgrade() -> None:
    op.drop_column('movie_recommendation_text', 'model')
    op.drop_column('movie_recommendation_text', 'source')
    op.drop_index('ix_movie_recommendation_text_movie_id', table_name='movie_recommendation_text')

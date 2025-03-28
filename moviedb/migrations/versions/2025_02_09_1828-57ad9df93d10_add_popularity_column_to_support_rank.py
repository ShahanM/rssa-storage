"""add popularity column to support rank

Revision ID: 57ad9df93d10
Revises: a9db55279788
Create Date: 2025-02-09 18:28:53.696029

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57ad9df93d10'
down_revision: Union[str, None] = 'a9db55279788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movies', sa.Column('imdb_popularity', sa.Numeric(), nullable=True))
    op.add_column('movies', sa.Column('tmdb_popularity', sa.Numeric(), nullable=True))


def downgrade() -> None:
    op.drop_column('movies', 'tmdb_popularity')
    op.drop_column('movies', 'imdb_popularity')

"""drop movie_ids column from pre shuffled movie list

Revision ID: ac59e9e5273f
Revises: eb61c804ff41
Create Date: 2026-03-27 23:57:58.474944

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = 'ac59e9e5273f'
down_revision: str | None = 'eb61c804ff41'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column('pre_shuffled_movie_lists', 'movie_ids')


def downgrade() -> None:
    op.add_column(
        'pre_shuffled_movie_lists',
        sa.Column('movie_ids', postgresql.ARRAY(sa.UUID()), autoincrement=False, nullable=True),
    )

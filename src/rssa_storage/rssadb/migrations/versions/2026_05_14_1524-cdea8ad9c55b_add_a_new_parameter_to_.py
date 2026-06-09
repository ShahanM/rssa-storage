"""add a new parameter to preshuffledmovielist

Revision ID: cdea8ad9c55b
Revises: d45bf52d0611
Create Date: 2026-05-14 15:24:03.058859

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'cdea8ad9c55b'
down_revision: str | None = 'd45bf52d0611'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('pre_shuffled_movie_lists', sa.Column('active_anchor_limit', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('pre_shuffled_movie_lists', 'active_anchor_limit')

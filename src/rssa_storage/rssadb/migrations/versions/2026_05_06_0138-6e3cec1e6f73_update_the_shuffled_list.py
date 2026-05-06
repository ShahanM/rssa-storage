"""update the shuffled list

Revision ID: 6e3cec1e6f73
Revises: 094a714ae057
Create Date: 2026-05-06 01:38:46.310008

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '6e3cec1e6f73'
down_revision: str | None = '094a714ae057'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('pre_shuffled_movie_lists', sa.Column('movie_ids', sa.ARRAY(sa.UUID()), nullable=False))


def downgrade() -> None:
    op.drop_column('pre_shuffled_movie_lists', 'movie_ids')

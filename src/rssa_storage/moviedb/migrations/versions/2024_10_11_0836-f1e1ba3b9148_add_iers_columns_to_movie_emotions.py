"""add ieRS columns to movie_emotions

Revision ID: f1e1ba3b9148
Revises: d59bbff60509
Create Date: 2024-10-11 08:36:01.070771

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f1e1ba3b9148'
down_revision: str | None = 'd59bbff60509'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('movie_emotions', sa.Column('iers_count', sa.Integer, nullable=False))
    op.add_column('movie_emotions', sa.Column('iers_rank', sa.Integer, nullable=False))


def downgrade() -> None:
    op.drop_column('movie_emotions', 'iers_count')
    op.drop_column('movie_emotions', 'iers_rank')

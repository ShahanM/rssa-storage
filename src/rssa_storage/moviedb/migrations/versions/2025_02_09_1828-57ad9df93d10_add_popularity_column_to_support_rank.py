"""add popularity column to support rank

Revision ID: 57ad9df93d10
Revises: a9db55279788
Create Date: 2025-02-09 18:28:53.696029

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '57ad9df93d10'
down_revision: str | None = 'a9db55279788'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('movies', sa.Column('imdb_popularity', sa.Numeric(), nullable=True))
    op.add_column('movies', sa.Column('tmdb_popularity', sa.Numeric(), nullable=True))


def downgrade() -> None:
    op.drop_column('movies', 'tmdb_popularity')
    op.drop_column('movies', 'imdb_popularity')

"""add completion code and redirect url columns to studies

Revision ID: 7509aefa820b
Revises: debba4907b4a
Create Date: 2026-03-26 13:43:57.216609

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '7509aefa820b'
down_revision: str | None = 'debba4907b4a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('studies', sa.Column('completion_code', sa.String(), nullable=True))
    op.add_column('studies', sa.Column('redirect_url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('studies', 'redirect_url')
    op.drop_column('studies', 'completion_code')

"""add is_negative to survey_items

Revision ID: 0100e2b78a86
Revises: 54fdaea3fde4
Create Date: 2026-07-08 15:57:05.300789

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '0100e2b78a86'
down_revision: str | None = '54fdaea3fde4'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'survey_items', sa.Column('is_negative', sa.Boolean(), server_default=sa.text('false'), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('survey_items', 'is_negative')

"""add optional view_link_key column to study_conditions

Revision ID: 22694afb84f5
Revises: 9aa5451ca1ae
Create Date: 2026-01-20 12:57:44.715463

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '22694afb84f5'
down_revision: str | None = '9aa5451ca1ae'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'study_conditions',
        sa.Column(
            'view_link_key',
            sa.String(length=48),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column('study_conditions', 'view_link_key')

"""Sync participant_demographics tables with sqlalchemy models

Revision ID: 7c61de772826
Revises: bc7ecadba30e
Create Date: 2026-01-05 21:54:08.526364

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7c61de772826'
down_revision: str | None = 'bc7ecadba30e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'participant_demographics',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_demographics',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        'participant_demographics',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'participant_demographics',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )

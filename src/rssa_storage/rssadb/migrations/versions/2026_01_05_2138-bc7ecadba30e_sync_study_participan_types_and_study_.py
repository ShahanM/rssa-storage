"""Sync study_participan_types, and study_participants tables with sqlalchemy models

Revision ID: bc7ecadba30e
Revises: b9bf554bd2b7
Create Date: 2026-01-05 21:38:26.974517

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc7ecadba30e'
down_revision: str | None = 'b9bf554bd2b7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'study_participant_types',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'study_participants',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'study_participants',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'study_participants',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        'study_participants',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'study_participants',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column('study_participants', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)
    op.alter_column(
        'study_participant_types', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False
    )

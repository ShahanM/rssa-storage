"""Sync studies tables with sqlalchemy models

Revision ID: 5aacc1ba5ab0
Revises: 08a92578f639
Create Date: 2026-01-05 13:32:48.597279

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5aacc1ba5ab0'
down_revision: str | None = '08a92578f639'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'studies', 'id', existing_type=sa.UUID(), server_default=sa.text('gen_random_uuid()'), existing_nullable=False
    )
    op.alter_column(
        'studies',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'studies',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        'studies', 'updated_at', existing_type=postgresql.TIMESTAMP(timezone=True), server_default=None, nullable=True
    )
    op.alter_column(
        'studies',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column('studies', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)

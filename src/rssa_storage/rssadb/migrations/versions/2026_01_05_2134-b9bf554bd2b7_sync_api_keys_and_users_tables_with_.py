"""Sync api_keys, and users tables with sqlalchemy models

Revision ID: b9bf554bd2b7
Revises: f778ee8012d9
Create Date: 2026-01-05 21:34:01.108143

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9bf554bd2b7'
down_revision: str | None = 'f778ee8012d9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'api_keys', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.alter_column(
        'api_keys',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.add_column(
        'users', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.alter_column(
        'users',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )


def downgrade() -> None:
    op.alter_column(
        'users',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.drop_column('users', 'updated_at')
    op.alter_column(
        'api_keys',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.drop_column('api_keys', 'updated_at')

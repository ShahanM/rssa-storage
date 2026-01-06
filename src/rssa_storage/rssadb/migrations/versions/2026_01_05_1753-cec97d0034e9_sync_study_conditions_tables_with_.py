"""Sync study_conditions tables with sqlalchemy models

Revision ID: cec97d0034e9
Revises: 5aacc1ba5ab0
Create Date: 2026-01-05 17:53:46.286744

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cec97d0034e9'
down_revision: str | None = '5aacc1ba5ab0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'study_conditions',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'study_conditions',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'study_conditions',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )
    op.drop_constraint(op.f('fk_study_conditions_created_by_id'), 'study_conditions', type_='foreignkey')
    op.drop_column('study_conditions', 'created_by_id')


def downgrade() -> None:
    op.add_column('study_conditions', sa.Column('created_by_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(
        op.f('fk_study_conditions_created_by_id'),
        'study_conditions',
        'users',
        ['created_by_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.alter_column(
        'study_conditions',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    op.alter_column(
        'study_conditions',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column('study_conditions', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)

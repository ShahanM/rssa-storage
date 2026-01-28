"""Add study authorization table

Revision ID: 1ab4cc504a9d
Revises: 22694afb84f5
Create Date: 2026-01-28 00:17:21.502397

"""

import uuid
from collections.abc import Sequence
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


revision: str = '1ab4cc504a9d'
down_revision: str | None = '22694afb84f5'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'study_authorizations',
        sa.Column('study_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['study_id'], ['studies.id'], name=op.f('fk_study_authorizations_study_id'), ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk_study_authorizations_user_id'), ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_study_authorizations')),
        sa.UniqueConstraint('study_id', 'user_id', name=op.f('uq_study_authorizations_study_id_user_id')),
    )
    op.create_index(op.f('ix_study_authorizations_user_id'), 'study_authorizations', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_study_authorizations_user_id'), table_name='study_authorizations')
    op.drop_table('study_authorizations')

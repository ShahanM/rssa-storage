"""Sync study_step_pages tables with sqlalchemy models

Revision ID: 7b29af2b0960
Revises: ef40ee719e14
Create Date: 2026-01-05 21:23:11.389357

"""

import uuid
from collections.abc import Sequence
from datetime import datetime, timezone

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7b29af2b0960'
down_revision: str | None = 'ef40ee719e14'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'study_step_pages',
        'page_type',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='Type of page, e.g., "survey" or "null" for non-survey pages',
        existing_nullable=True,
    )
    op.alter_column('study_step_pages', 'title', existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True)
    op.alter_column(
        'study_step_pages', 'instructions', existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
    )
    op.alter_column(
        'study_step_pages',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'study_step_pages',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'study_step_pages',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )
    op.drop_constraint(op.f('uq_study_step_pages'), 'study_step_pages', type_='unique')
    op.create_unique_constraint(
        op.f('uq_study_step_pages_study_step_id_order_position'),
        'study_step_pages',
        ['study_step_id', 'order_position'],
    )
    op.drop_constraint(op.f('fk_study_step_pages_created_by_id'), 'study_step_pages', type_='foreignkey')
    op.drop_column('study_step_pages', 'created_by_id')


def downgrade() -> None:
    op.add_column('study_step_pages', sa.Column('created_by_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(
        op.f('fk_study_step_pages_created_by_id'),
        'study_step_pages',
        'users',
        ['created_by_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.drop_constraint(op.f('uq_study_step_pages_study_step_id_order_position'), 'study_step_pages', type_='unique')
    op.create_unique_constraint(
        op.f('uq_study_step_pages'),
        'study_step_pages',
        ['study_step_id', 'order_position'],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        'study_step_pages',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    op.alter_column(
        'study_step_pages',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column('study_step_pages', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)
    op.alter_column(
        'study_step_pages', 'instructions', existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True
    )
    op.alter_column('study_step_pages', 'title', existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column(
        'study_step_pages',
        'page_type',
        existing_type=sa.VARCHAR(),
        comment='Type of page, e.g., "survey" or "null" for non-survey pages',
        existing_nullable=True,
    )

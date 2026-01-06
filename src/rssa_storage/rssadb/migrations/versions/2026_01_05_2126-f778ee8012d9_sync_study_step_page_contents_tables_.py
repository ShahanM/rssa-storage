"""Sync study_step_page_contents tables with sqlalchemy models

Revision ID: f778ee8012d9
Revises: 7b29af2b0960
Create Date: 2026-01-05 21:26:19.260966

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f778ee8012d9'
down_revision: str | None = '7b29af2b0960'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'study_step_page_contents', 'preamble', existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
    )
    op.alter_column('study_step_page_contents', 'survey_scale_id', existing_type=sa.UUID(), nullable=False)
    op.alter_column(
        'study_step_page_contents',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'study_step_page_contents',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )
    op.drop_constraint(
        op.f('fk_study_step_page_contents_created_by_id'), 'study_step_page_contents', type_='foreignkey'
    )
    op.drop_column('study_step_page_contents', 'created_by_id')


def downgrade() -> None:
    op.add_column('study_step_page_contents', sa.Column('created_by_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(
        op.f('fk_study_step_page_contents_created_by_id'),
        'study_step_page_contents',
        'users',
        ['created_by_id'],
        ['id'],
        ondelete='SET NULL',
    )
    op.alter_column(
        'study_step_page_contents',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    op.alter_column(
        'study_step_page_contents',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column('study_step_page_contents', 'survey_scale_id', existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        'study_step_page_contents', 'preamble', existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True
    )

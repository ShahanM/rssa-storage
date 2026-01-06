"""Sync study_steps tables with sqlalchemy models

Revision ID: ef40ee719e14
Revises: cec97d0034e9
Create Date: 2026-01-05 21:19:09.356435

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ef40ee719e14'
down_revision: str | None = 'cec97d0034e9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'study_steps',
        'step_type',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='Type of step - "survey", "preference-elicitation", "study-information","interaction", and "demographics',
        existing_nullable=True,
    )
    op.alter_column('study_steps', 'title', existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True)
    op.alter_column('study_steps', 'instructions', existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True)
    op.alter_column(
        'study_steps',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'study_steps',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'study_steps',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )
    op.drop_constraint(op.f('study_step_study_id_order_position_key'), 'study_steps', type_='unique')
    op.drop_constraint(op.f('uq_study_steps'), 'study_steps', type_='unique')
    op.create_unique_constraint(
        op.f('uq_study_steps_study_id_order_position'), 'study_steps', ['study_id', 'order_position']
    )
    op.create_unique_constraint(
        op.f('uq_study_steps_study_id_path'), 'study_steps', ['study_id', 'path'], deferrable=True, initially='deferred'
    )
    op.drop_constraint(op.f('fk_study_steps_created_by_id'), 'study_steps', type_='foreignkey')
    op.drop_column('study_steps', 'created_by_id')


def downgrade() -> None:
    op.add_column('study_steps', sa.Column('created_by_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(
        op.f('fk_study_steps_created_by_id'), 'study_steps', 'users', ['created_by_id'], ['id'], ondelete='SET NULL'
    )
    op.drop_constraint(op.f('uq_study_steps_study_id_path'), 'study_steps', type_='unique')
    op.drop_constraint(op.f('uq_study_steps_study_id_order_position'), 'study_steps', type_='unique')
    op.create_unique_constraint(
        op.f('uq_study_steps'), 'study_steps', ['study_id', 'path'], postgresql_nulls_not_distinct=False
    )
    op.create_unique_constraint(
        op.f('study_step_study_id_order_position_key'),
        'study_steps',
        ['study_id', 'order_position'],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        'study_steps',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    op.alter_column(
        'study_steps',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column('study_steps', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)
    op.alter_column('study_steps', 'instructions', existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column('study_steps', 'title', existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column(
        'study_steps',
        'step_type',
        existing_type=sa.VARCHAR(),
        comment='Type of step - "survey", "preference-elicitation", "study-information","interaction", and "demographics',
        existing_nullable=True,
    )

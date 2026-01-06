"""sync test

Revision ID: a587b7ffa799
Revises: 848348482191
Create Date: 2026-01-05 23:45:59.578461

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a587b7ffa799'
down_revision: str | None = '848348482191'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index(op.f('ix_permissions_auth0_user_id'), table_name='permissions')
    op.drop_index(op.f('ix_permissions_study_id'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_table('access_logs')


def downgrade() -> None:
    op.create_table(
        'access_logs',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('auth0_user', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('action', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('resource', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('resource_id', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('timestamp', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_access_logs')),
    )
    op.create_table(
        'permissions',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('permission_name', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('study_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('auth0_user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_permissions')),
        sa.UniqueConstraint(
            'permission_name',
            'study_id',
            name=op.f('uq_permissions'),
            postgresql_include=[],
            postgresql_nulls_not_distinct=False,
        ),
    )
    op.create_index(op.f('ix_permissions_study_id'), 'permissions', ['study_id'], unique=False)
    op.create_index(op.f('ix_permissions_auth0_user_id'), 'permissions', ['auth0_user_id'], unique=False)

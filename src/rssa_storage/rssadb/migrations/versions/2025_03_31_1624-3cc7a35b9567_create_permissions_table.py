"""Create permissions table

Revision ID: 3cc7a35b9567
Revises: c6c1107c2c83
Create Date: 2025-03-31 16:24:00.394875

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '3cc7a35b9567'
down_revision: str | None = 'c6c1107c2c83'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'permissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('permission_name', sa.String(), nullable=False),
        sa.Column('study_id', UUID(as_uuid=True), nullable=False),
        sa.Column('auth0_user_id', sa.String(), nullable=False),
        sa.UniqueConstraint('permission_name', 'study_id', name='uq_permission_name_study_id'),
        sa.ForeignKeyConstraint(['study_id'], ['study.id'], name='fk_permissions_study_id', ondelete='CASCADE'),
    )
    op.create_index('ix_permissions_study_id', 'permissions', ['study_id'])
    op.create_index('ix_permissions_auth0_user_id', 'permissions', ['auth0_user_id'])


def downgrade() -> None:
    op.drop_index('ix_permissions_auth0_user_id', 'permissions')
    op.drop_index('ix_permissions_study_id', 'permissions')
    op.drop_table('permissions')

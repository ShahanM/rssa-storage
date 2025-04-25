"""add created_by and owner columns to the study table

Revision ID: c6c1107c2c83
Revises: 2c5df8f6ec05
Create Date: 2025-03-31 16:18:58.744816

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6c1107c2c83'
down_revision: Union[str, None] = '2c5df8f6ec05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'study',
        sa.Column('created_by', sa.String(), nullable=True)
    )
    op.add_column(
        'study',
        sa.Column('owner', sa.String(), nullable=True)
    )
    op.create_index('ix_study_created_by', 'study', ['created_by'])
    op.create_index('ix_study_owner', 'study', ['owner'])
    op.create_index('ix_study_created_by_owner', 'study', ['created_by', 'owner'])


def downgrade() -> None:
    op.drop_index('ix_study_created_by_owner', 'study')
    op.drop_index('ix_study_owner', 'study')
    op.drop_index('ix_study_created_by', 'study')
    op.drop_column('study', 'owner')
    op.drop_column('study', 'created_by')

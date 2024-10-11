"""add recommendation_count column to study_condition

Revision ID: 64e9eabe86b9
Revises: e702e5bd1477
Create Date: 2024-10-08 14:28:49.574207

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64e9eabe86b9'
down_revision: Union[str, None] = 'e702e5bd1477'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('study_condition',
        sa.Column('recommendation_count', sa.Integer, default=10))
    op.execute('UPDATE study_condition SET recommendation_count = 10')
    op.alter_column('study_condition', 'recommendation_count', nullable=False)


def downgrade() -> None:
    op.drop_column('study_condition', 'recommendation_count')


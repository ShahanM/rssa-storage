"""Add description column to study_condition

Revision ID: 9ed2a79b1c93
Revises: a0a51a03c3df
Create Date: 2024-08-16 14:28:49.027547

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ed2a79b1c93'
down_revision: Union[str, None] = 'a0a51a03c3df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('study_condition',
        sa.Column('description', sa.String, nullable=True)
    )


def downgrade() -> None:
    op.drop_column('study_condition', 'description')

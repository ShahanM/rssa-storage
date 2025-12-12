"""add recommender_key to study_conditions table

This migration adds a new column 'recommender_key' to the 'study_conditions' table.
This column is used to store the registry key mapped to a specific recommender function.

Revision ID: 5af952aa36e6
Revises: dc77bda9b96e
Create Date: 2025-12-11 15:43:29.390420

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5af952aa36e6'
down_revision: Union[str, None] = 'dc77bda9b96e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('study_conditions', sa.Column('recommender_key', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('study_conditions', 'recommender_key')

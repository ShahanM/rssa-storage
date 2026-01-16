"""add recommender_key to study_conditions table

This migration adds a new column 'recommender_key' to the 'study_conditions' table.
This column is used to store the registry key mapped to a specific recommender function.

Revision ID: 5af952aa36e6
Revises: dc77bda9b96e
Create Date: 2025-12-11 15:43:29.390420

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5af952aa36e6'
down_revision: str | None = 'dc77bda9b96e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('study_conditions', sa.Column('recommender_key', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('study_conditions', 'recommender_key')

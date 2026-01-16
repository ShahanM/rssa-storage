"""add order_position and rename level to value on scale_level table

Revision ID: bd2a693f37ad
Revises: 4d55eb38447e
Create Date: 2025-08-11 14:17:49.778464

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bd2a693f37ad'
down_revision: str | None = '4d55eb38447e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('scale_level', sa.Column('order_position', sa.Integer(), nullable=True))
    print("Added nullable 'order_position' column to 'scale_level'.")

    op.execute('UPDATE scale_level SET order_position = level')
    print("Copied data from 'level' to 'order_position'.")

    op.alter_column('scale_level', 'order_position', nullable=False)
    print("Made 'order_position' column non-nullable.")

    op.alter_column('scale_level', 'level', new_column_name='value')
    print("Renamed 'level' column to 'value'.")


def downgrade() -> None:
    op.alter_column('scale_level', 'value', new_column_name='level')
    print("Renamed 'value' column back to 'level'.")

    op.drop_column('scale_level', 'order_position')
    print("Dropped 'order_position' column from 'scale_level'.")

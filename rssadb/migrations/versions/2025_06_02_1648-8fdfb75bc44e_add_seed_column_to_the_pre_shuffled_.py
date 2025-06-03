"""add seed column to the pre shuffled movie list

Revision ID: 8fdfb75bc44e
Revises: 1208b82ddbf4
Create Date: 2025-06-02 16:48:24.883092

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8fdfb75bc44e"
down_revision: Union[str, None] = "1208b82ddbf4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "pre_shuffled_movie_lists", sa.Column("seed", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("pre_shuffled_movie_lists", "seed")

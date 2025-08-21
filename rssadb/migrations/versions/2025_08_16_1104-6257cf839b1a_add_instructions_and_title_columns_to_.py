"""add instructions and title columns to step_page

Revision ID: 6257cf839b1a
Revises: c39207ae1388
Create Date: 2025-08-16 11:04:12.094820

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6257cf839b1a"
down_revision: Union[str, None] = "c39207ae1388"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("step_page", sa.Column("title", sa.String(), nullable=True))
    op.add_column("step_page", sa.Column("instructions", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("step_page", "title")
    op.drop_column("step_page", "instructions")

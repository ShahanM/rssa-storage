"""alter timestamp for step page

Revision ID: 82f0310a94f6
Revises: 7d2872a8e8cf
Create Date: 2025-06-30 22:52:35.346440

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "82f0310a94f6"
down_revision: Union[str, None] = "7d2872a8e8cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "step_page",
        "date_created",
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )


def downgrade() -> None:
    op.alter_column(
        "step_page",
        "date_created",
        type_=sa.DateTime,
        existing_type=sa.TIMESTAMP(timezone=True),
    )

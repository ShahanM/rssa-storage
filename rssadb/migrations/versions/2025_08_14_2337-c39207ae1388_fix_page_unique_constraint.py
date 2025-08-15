"""fix_page_unique_constraint

Revision ID: c39207ae1388
Revises: bd2a693f37ad
Create Date: 2025-08-14 23:37:27.851999

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c39207ae1388"
down_revision: Union[str, None] = "bd2a693f37ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("page_study_id_step_id_order_position_key", table_name="step_page")

    op.create_index(
        "ix_step_page_study_step_page_order",
        "step_page",
        ["study_id", "step_id", "id", "order_position"],
        unique=True,
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index("ix_step_page_study_step_page_order", table_name="step_page")

    op.create_index(
        "page_study_id_step_id_order_position_key",
        "step_page",
        ["study_id", "step_id", "order_position"],
        unique=True,
    )

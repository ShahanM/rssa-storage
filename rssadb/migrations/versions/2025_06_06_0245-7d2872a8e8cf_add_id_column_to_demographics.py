"""add id column to demographics

Revision ID: 7d2872a8e8cf
Revises: aa841494c45c
Create Date: 2025-06-06 02:45:26.038750

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d2872a8e8cf"
down_revision: Union[str, None] = "aa841494c45c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("demographics_pkey", "demographics", type_="primary")
    op.add_column(
        "demographics",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE demographics
        SET id = gen_random_uuid()
        WHERE id IS NULL;
        """
    )

    with op.batch_alter_table("demographics", schema=None) as batch_op:
        batch_op.alter_column("id", existing_type=UUID(as_uuid=True), nullable=False)

    op.create_primary_key("demographics_pkey", "demographics", ["id"])


def downgrade() -> None:
    op.drop_constraint("demographics_pkey", "demographics", type_="primary")
    op.drop_column("demographics", "id")
    op.create_primary_key("demographics_pkey", "demographics", ["participant_id"])

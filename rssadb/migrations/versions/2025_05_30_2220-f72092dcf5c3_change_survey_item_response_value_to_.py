"""change survey_item_response value to foreign key on scale_level

Revision ID: f72092dcf5c3
Revises: 6aefb18a22ad
Create Date: 2025-05-30 22:20:46.044381

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f72092dcf5c3"
down_revision: Union[str, None] = "6aefb18a22ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("survey_item_response", "response_value")

    op.add_column(
        "survey_item_response",
        sa.Column("response", UUID(as_uuid=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_survey_item_response_scale_level_id",
        "survey_item_response",
        "scale_level",
        ["response"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_survey_item_response_scale_level_id",
        "survey_item_response",
        type_="foreignkey",
    )

    op.drop_column("survey_item_response", "response")

    op.add_column(
        "survey_item_response", sa.Column("response_value", sa.String(), nullable=False)
    )

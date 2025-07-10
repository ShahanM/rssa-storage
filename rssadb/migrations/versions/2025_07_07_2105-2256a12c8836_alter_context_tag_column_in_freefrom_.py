"""alter context_tag column in freefrom_response to be unbound

Revision ID: 2256a12c8836
Revises: 6912b533545a
Create Date: 2025-07-07 21:05:20.145371

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2256a12c8836"
down_revision: Union[str, None] = "6912b533545a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "freeform_response",
        "context_tag",
        existing_type=sa.String(length=50),
        type_=sa.Text,
        existing_nullable=True,
        nullable=True,
        posgresql_using="context_tag::text",
    )


def downgrade() -> None:
    op.alter_column(
        "freeform_response",
        "context_tag",
        existing_type=sa.Text,
        type_=sa.String(length=50),
        existing_nullable=True,
        nullable=True,
        posgresql_using="SUBSTRING(my_column FROM 1 FOR 50)::varchar(50)",
    )

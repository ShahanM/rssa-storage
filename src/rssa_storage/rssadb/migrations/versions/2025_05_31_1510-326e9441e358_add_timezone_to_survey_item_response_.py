"""add timezone to survey_item_response dates

Revision ID: 326e9441e358
Revises: f72092dcf5c3
Create Date: 2025-05-31 15:10:37.692767

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '326e9441e358'
down_revision: str | None = 'f72092dcf5c3'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'survey_item_response',
        'date_created',
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )

    op.alter_column(
        'survey_item_response',
        'date_modified',
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )


def downgrade() -> None:
    op.alter_column(
        'survey_item_response',
        'date_created',
        type_=sa.DateTime,
        existing_type=sa.TIMESTAMP(timezone=True),
    )
    op.alter_column(
        'survey_item_response',
        'date_modified',
        type_=sa.DateTime,
        existing_type=sa.TIMESTAMP(timezone=True),
    )

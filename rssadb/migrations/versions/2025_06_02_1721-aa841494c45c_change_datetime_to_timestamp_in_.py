"""change datetime to timestamp in preshuffled list and movie session

Revision ID: aa841494c45c
Revises: 8fdfb75bc44e
Create Date: 2025-06-02 17:21:34.307454

"""

from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aa841494c45c"
down_revision: Union[str, None] = "8fdfb75bc44e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "participant_movie_sessions",
        "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )
    op.alter_column(
        "participant_movie_sessions",
        "last_accessed_at",
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )
    op.alter_column(
        "pre_shuffled_movie_lists",
        "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )


def downgrade() -> None:
    op.alter_column(
        "participant_movie_sessions",
        "created_at",
        type_=sa.DateTime,
        existing_type=sa.TIMESTAMP(timezone=True),
    )
    op.alter_column(
        "participant_movie_sessions",
        "last_accessed_at",
        type_=sa.DateTime,
        existing_type=sa.TIMESTAMP(timezone=True),
    )

    op.alter_column(
        "pre_shuffled_movie_lists",
        "created_at",
        type_=sa.DateTime,
        existing_type=sa.TIMESTAMP(timezone=True),
    )

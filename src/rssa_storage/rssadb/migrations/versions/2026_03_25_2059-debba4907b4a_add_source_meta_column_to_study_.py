"""add source_meta column to study_participants

Revision ID: debba4907b4a
Revises: 7ab04095d69b
Create Date: 2026-03-25 20:59:28.055648

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = 'debba4907b4a'
down_revision: str | None = '7ab04095d69b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'study_participants', sa.Column('source_meta', postgresql.JSONB(astext_type=sa.Text()), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('study_participants', 'source_meta')

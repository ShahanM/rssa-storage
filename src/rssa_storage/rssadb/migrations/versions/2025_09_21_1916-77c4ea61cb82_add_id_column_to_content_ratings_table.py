"""Add ID column to content_ratings table

Revision ID: 77c4ea61cb82
Revises: 5cf6f96ba737
Create Date: 2025-09-21 19:16:14.916715

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '77c4ea61cb82'
down_revision: str | None = '5cf6f96ba737'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('TRUNCATE TABLE content_ratings CASCADE;')
    op.add_column('content_ratings', sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False))


def downgrade() -> None:
    op.drop_column('content_ratings', 'id')

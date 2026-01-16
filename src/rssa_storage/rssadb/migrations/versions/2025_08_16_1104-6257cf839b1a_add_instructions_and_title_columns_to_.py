"""add instructions and title columns to step_page

Revision ID: 6257cf839b1a
Revises: c39207ae1388
Create Date: 2025-08-16 11:04:12.094820

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6257cf839b1a'
down_revision: str | None = 'c39207ae1388'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('step_page', sa.Column('title', sa.String(), nullable=True))
    op.add_column('step_page', sa.Column('instructions', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('step_page', 'title')
    op.drop_column('step_page', 'instructions')

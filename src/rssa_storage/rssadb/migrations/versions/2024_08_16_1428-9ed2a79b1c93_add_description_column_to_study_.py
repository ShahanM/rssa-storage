"""Add description column to study_condition

Revision ID: 9ed2a79b1c93
Revises: a0a51a03c3df
Create Date: 2024-08-16 14:28:49.027547

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9ed2a79b1c93'
down_revision: str | None = 'a0a51a03c3df'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('study_condition', sa.Column('description', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('study_condition', 'description')

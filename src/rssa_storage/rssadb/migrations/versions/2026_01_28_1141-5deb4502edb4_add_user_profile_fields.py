"""add user profile fields

Revision ID: 5deb4502edb4
Revises: 1ab4cc504a9d
Create Date: 2026-01-28 11:41:28.626053

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5deb4502edb4'
down_revision: str | None = '1ab4cc504a9d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    op.add_column('users', sa.Column('desc', sa.String(), nullable=True))
    op.add_column('users', sa.Column('picture', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'picture')
    op.drop_column('users', 'desc')
    op.drop_column('users', 'email')

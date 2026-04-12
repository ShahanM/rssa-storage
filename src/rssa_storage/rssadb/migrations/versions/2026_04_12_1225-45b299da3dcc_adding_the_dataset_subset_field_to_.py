"""adding the dataset subset field to studies

Revision ID: 45b299da3dcc
Revises: a12e2fa9a176
Create Date: 2026-04-12 12:25:34.966945

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '45b299da3dcc'
down_revision: str | None = 'a12e2fa9a176'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('studies', sa.Column('dataset_subset', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('studies', 'dataset_subset')

"""add title and instruction columns to study_step

Revision ID: 91c00d8fbb1d
Revises: 67dec0365681
Create Date: 2025-07-19 01:57:33.652657

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '91c00d8fbb1d'
down_revision: Union[str, None] = '67dec0365681'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column('study_step', sa.Column('title', sa.String(), nullable=True))
	op.add_column('study_step', sa.Column('instructions', sa.String(), nullable=True))


def downgrade() -> None:
	op.drop_column('study_step', 'title')
	op.drop_column('study_step', 'instructions')

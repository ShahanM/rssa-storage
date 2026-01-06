"""add instruction slug to the page_contents

Revision ID: 5cf6f96ba737
Revises: 010c1972590c
Create Date: 2025-09-20 00:06:32.842425

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5cf6f96ba737'
down_revision: Union[str, None] = '010c1972590c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column('page_contents', sa.Column('preamble', sa.String(), nullable=True))


def downgrade() -> None:
	op.drop_column('page_contents', 'preamble')

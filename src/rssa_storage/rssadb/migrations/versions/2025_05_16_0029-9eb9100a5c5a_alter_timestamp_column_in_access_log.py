"""alter timestamp column in access_log

Revision ID: 9eb9100a5c5a
Revises: 3cc7a35b9567
Create Date: 2025-05-16 00:29:40.497668

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9eb9100a5c5a'
down_revision: Union[str, None] = '3cc7a35b9567'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.alter_column(
		'access_log',
		'timestamp',
		type_=sa.TIMESTAMP(timezone=True),
		existing_type=sa.DateTime,
	)


def downgrade() -> None:
	op.alter_column(
		'access_log',
		'timestamp',
		type_=sa.DateTime,
		existing_type=sa.TIMESTAMP(timezone=True),
	)

"""alter timestamp column in participant table to timezone aware

Revision ID: 427509af80a1
Revises: 9eb9100a5c5a
Create Date: 2025-05-26 16:52:17.950600

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '427509af80a1'
down_revision: Union[str, None] = '9eb9100a5c5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.alter_column(
		'study_participant',
		'date_created',
		type_=sa.TIMESTAMP(timezone=True),
		existing_type=sa.DateTime,
	)
	op.alter_column(
		'study_participant',
		'date_updated',
		type_=sa.TIMESTAMP(timezone=True),
		existing_type=sa.DateTime,
	)


def downgrade() -> None:
	op.alter_column(
		'study_participant',
		'date_created',
		type_=sa.DateTime,
		existing_type=sa.TIMESTAMP(timezone=True),
	)
	op.alter_column(
		'study_participant',
		'date_updated',
		type_=sa.DateTime,
		existing_type=sa.TIMESTAMP(timezone=True),
	)

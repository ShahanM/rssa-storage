"""Add UUID primary key to scale_level

Revision ID: dd1d4ec486f5
Revises: 427509af80a1
Create Date: 2025-05-29 16:02:21.886979

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'dd1d4ec486f5'
down_revision: Union[str, None] = '427509af80a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column('scale_level', sa.Column('id', UUID(as_uuid=True), nullable=True))

	# connection = op.get_bind()
	with op.batch_alter_table('scale_level') as batch_op:
		batch_op.execute(sa.text('UPDATE scale_level SET id = gen_random_uuid()'))

	op.alter_column(
		'scale_level',
		'id',
		existing_type=UUID(as_uuid=True),
		nullable=False,
		existing_nullable=True,
	)

	op.create_primary_key('scale_level_pkey', 'scale_level', ['id'])


def downgrade() -> None:
	op.drop_constraint('scale_level_pkey', 'scale_level', type_='primary')
	op.drop_column('scale_level', 'id')

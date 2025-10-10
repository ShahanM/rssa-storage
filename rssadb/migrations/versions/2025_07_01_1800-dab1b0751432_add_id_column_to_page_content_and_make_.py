"""Add id column to page_content and make it primary key

Revision ID: dab1b0751432
Revises: 82f0310a94f6
Create Date: 2025-07-01 18:00:19.318123

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'dab1b0751432'
down_revision: Union[str, None] = '82f0310a94f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	with op.batch_alter_table('page_content', schema=None) as batch_op:
		batch_op.add_column(
			sa.Column(
				'id',
				UUID(as_uuid=True),
				nullable=True,
				server_default=sa.text('gen_random_uuid()'),
			)
		)

	with op.batch_alter_table('page_content', schema=None) as batch_op:
		batch_op.alter_column('id', existing_type=UUID(as_uuid=True), nullable=False)

	batch_op.create_primary_key('page_content_pkey', ['id'])
	batch_op.create_unique_constraint('uq_page_content_pair', ['page_id', 'content_id'])


def downgrade() -> None:
	with op.batch_alter_table('page_content', schema=None) as batch_op:
		batch_op.drop_constraint('uq_page_content_pair', type_='unique')

		batch_op.drop_constraint('page_content_pkey', type_='primary')

		batch_op.drop_column('id')

"""Add server default to all created_at columns

Revision ID: e16e67f2f146
Revises: d9f3e5afa748
Create Date: 2025-09-10 12:53:16.094899

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers, used by Alembic.
revision: str = 'e16e67f2f146'
down_revision: Union[str, None] = 'd9f3e5afa748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
	"""
	Finds all tables with a 'created_at' column and adds a server-side default
	value of transaction timestamp ('now()').
	"""
	print('Connecting to the database to inspect schema...')
	conn = op.get_bind()
	inspector = sa.inspect(conn)
	tables = inspector.get_table_names()

	print(f"Found {len(tables)} tables. Checking for 'created_at' columns...")

	for table_name in tables:
		columns = inspector.get_columns(table_name)
		has_created_at = any(c['name'] == 'created_at' for c in columns)

		if has_created_at:
			print(f"  -> Found 'created_at' in table '{table_name}'. Altering column...")
			try:
				op.alter_column(
					table_name,
					'created_at',
					server_default=sa.text('now()'),
					existing_type=TIMESTAMP(timezone=True),
					nullable=True,
				)
				print(f"     [SUCCESS] Applied server_default to '{table_name}.created_at'")
			except Exception as e:
				print(f"     [ERROR] Could not alter '{table_name}.created_at'. Reason: {e}")
	print('Upgrade script finished.')


def downgrade():
	"""
	Finds all tables with a 'created_at' column and removes the server-side default.
	"""
	print('Connecting to the database to inspect schema for downgrade...')
	conn = op.get_bind()
	inspector = sa.inspect(conn)
	tables = inspector.get_table_names()

	print(f"Found {len(tables)} tables. Checking for 'created_at' columns to revert...")

	for table_name in tables:
		columns = inspector.get_columns(table_name)
		has_created_at = any(c['name'] == 'created_at' for c in columns)

		if has_created_at:
			print(f"  -> Found 'created_at' in table '{table_name}'. Reverting column...")
			try:
				op.alter_column(
					table_name,
					'created_at',
					server_default=None,
					existing_type=TIMESTAMP(timezone=True),
					nullable=True,
				)
				print(f"     [SUCCESS] Removed server_default from '{table_name}.created_at'")
			except Exception as e:
				print(f"     [ERROR] Could not revert '{table_name}.created_at'. Reason: {e}")

	print('Downgrade script finished.')

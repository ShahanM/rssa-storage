"""Convert all timestamps to timezone-aware

Revision ID: d9f3e5afa748
Revises: 909053dba1d4
Create Date: 2025-09-09 23:29:31.368671

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd9f3e5afa748'
down_revision: Union[str, None] = '909053dba1d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	print("Finding and converting 'timestamp without time zone' columns to 'timestamp with time zone'...")

	conn = op.get_bind()
	columns_to_convert = conn.execute(
		sa.text("""
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type = 'timestamp without time zone'
        AND table_schema = 'public'; -- Adjust if you use a different schema
    """)
	).fetchall()

	if not columns_to_convert:
		print('No columns found to convert.')
		return

	for schema, table, column in columns_to_convert:
		print(f'Converting column: {schema}.{table}.{column}')

		op.execute(f"""
            ALTER TABLE {schema}.{table}
            ALTER COLUMN {column} TYPE TIMESTAMP WITH TIME ZONE
            USING {column} AT TIME ZONE 'UTC';
        """)

	print('Conversion complete.')


def downgrade() -> None:
	print("Finding and converting 'timestamp with time zone' columns back to 'timestamp without time zone'...")

	conn = op.get_bind()
	columns_to_revert = conn.execute(
		sa.text("""
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type = 'timestamp with time zone'
        AND table_schema = 'public'; -- Adjust if you use a different schema
    """)
	).fetchall()

	if not columns_to_revert:
		print('No columns found to revert.')
		return

	for schema, table, column in columns_to_revert:
		print(f'Reverting column: {schema}.{table}.{column}')
		op.execute(f"""
            ALTER TABLE {schema}.{table}
            ALTER COLUMN {column} TYPE TIMESTAMP WITHOUT TIME ZONE;
        """)

	print('Reversion complete.')

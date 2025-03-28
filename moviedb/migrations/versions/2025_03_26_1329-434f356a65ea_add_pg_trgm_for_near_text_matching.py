"""add pg_trgm for near text matching

Revision ID: 434f356a65ea
Revises: e604326a288c
Create Date: 2025-03-26 13:29:26.329954

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '434f356a65ea'
down_revision: Union[str, None] = 'e604326a288c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the index name and table name
index_name = 'idx_movie_title_trgm'
table_name = 'movies'

def upgrade() -> None:
	# Enable the pg_trgm extension (as before)
	op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

	# Create the trigram index on the title column
	op.create_index(
		index_name,
		table_name,
		[sa.text('title gin_trgm_ops')],
		postgresql_using='gin'
	)


def downgrade() -> None:
	# Drop the index
	op.drop_index(index_name, table_name)

	# Disable the pg_trgm extension
	op.execute("DROP EXTENSION IF EXISTS pg_trgm;")


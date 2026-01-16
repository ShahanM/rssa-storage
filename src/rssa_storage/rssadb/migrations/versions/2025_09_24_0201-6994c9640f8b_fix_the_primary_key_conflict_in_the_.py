"""fix the primary key conflict in the content_ratings table

Revision ID: 6994c9640f8b
Revises: 55788cd1de27
Create Date: 2025-09-24 02:01:18.296322

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6994c9640f8b'
down_revision: str | None = '55788cd1de27'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint('participant_content_rating_pkey', 'content_ratings', type_='primary')

    op.create_primary_key('content_ratings_pkey', 'content_ratings', ['id'])


def downgrade() -> None:
    op.drop_constraint('content_ratings_pkey', 'content_ratings', type_='primary')

    op.create_primary_key(
        'participant_content_rating_pkey', 'content_ratings', ['participant_id', 'item_id', 'item_table_name']
    )

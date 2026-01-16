"""create pre shuffled movie lists table

Revision ID: 27aeaf12b4d4
Revises: 326e9441e358
Create Date: 2025-06-02 14:27:52.120431

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY, UUID

# revision identifiers, used by Alembic.
revision: str = '27aeaf12b4d4'
down_revision: str | None = '326e9441e358'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'pre_shuffled_movie_lists',
        sa.Column('list_id', sa.Integer(), sa.Identity(), primary_key=True, autoincrement=True),
        sa.Column('subset_desc', sa.String, nullable=True),
        sa.Column('movie_ids', ARRAY(UUID(as_uuid=True)), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table('pre_shuffled_movie_lists')

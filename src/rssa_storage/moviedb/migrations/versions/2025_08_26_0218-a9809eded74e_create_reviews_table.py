"""create reviews table

Revision ID: a9809eded74e
Revises: 434f356a65ea
Create Date: 2025-08-26 02:18:38.755705

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a9809eded74e'
down_revision: str | None = '434f356a65ea'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'reviews',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('movie_id', sa.UUID(), nullable=False),
        sa.Column('review_id', sa.String(length=255), nullable=False),
        sa.Column('review_text', sa.Text(), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('scraped_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('review_id', name='uq_review_id'),
    )

    op.create_index(op.f('ix_reviews_movie_id'), 'reviews', ['movie_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_reviews_movie_id'), table_name='reviews')
    op.drop_table('reviews')

"""upgrading the shuffled movie indexing

Revision ID: eb61c804ff41
Revises: 7509aefa820b
Create Date: 2026-03-27 17:53:06.130945

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = 'eb61c804ff41'
down_revision: str | None = '7509aefa820b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'shuffled_movie_list_items',
        sa.Column('shuffle_list_id', sa.UUID(), nullable=False),
        sa.Column('movie_id', sa.UUID(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['shuffle_list_id'],
            ['pre_shuffled_movie_lists.id'],
            name=op.f('fk_shuffled_movie_list_items_shuffle_list_id'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_shuffled_movie_list_items')),
    )
    op.create_index(
        op.f('ix_shuffled_movie_list_items_shuffle_list_id_position'),
        'shuffled_movie_list_items',
        ['shuffle_list_id', 'position'],
        unique=False,
    )
    op.create_index(
        op.f('ix_shuffled_movie_list_items_shuffle_list_id'),
        'shuffled_movie_list_items',
        ['shuffle_list_id'],
        unique=False,
    )
    op.alter_column('pre_shuffled_movie_lists', 'movie_ids', existing_type=postgresql.ARRAY(sa.UUID()), nullable=True)


def downgrade() -> None:
    op.alter_column('pre_shuffled_movie_lists', 'movie_ids', existing_type=postgresql.ARRAY(sa.UUID()), nullable=False)
    op.drop_index(op.f('ix_shuffled_movie_list_items_shuffle_list_id'), table_name='shuffled_movie_list_items')
    op.drop_index(op.f('ix_shuffled_movie_list_items_shuffle_list_id_position'), table_name='shuffled_movie_list_items')
    op.drop_table('shuffled_movie_list_items')

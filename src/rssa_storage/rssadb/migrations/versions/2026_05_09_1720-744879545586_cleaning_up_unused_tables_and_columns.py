"""cleaning up unused tables and columns

Revision ID: 744879545586
Revises: 6e3cec1e6f73
Create Date: 2026-05-09 17:20:50.183713

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '744879545586'
down_revision: str | None = '6e3cec1e6f73'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index(op.f('ix_shuffled_movie_list_items_shuffle_list_id'), table_name='shuffled_movie_list_items')
    op.drop_index(op.f('ix_shuffled_movie_list_items_shuffle_list_id_position'), table_name='shuffled_movie_list_items')
    op.drop_table('shuffled_movie_list_items')

    op.add_column(
        'study_participants', sa.Column('is_verified', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False)
    )

    op.drop_column('study_participants', 'external_id')

    op.drop_constraint(
        op.f('fk_study_participants_study_participant_type_id'), 'study_participants', type_='foreignkey'
    )
    op.drop_column('study_participants', 'study_participant_type_id')
    op.drop_table('study_participant_types')


def downgrade() -> None:
    op.drop_column('study_participants', 'is_verified')

    op.add_column('study_participants', sa.Column('external_id', sa.VARCHAR(), autoincrement=False, nullable=True))

    op.create_table(
        'study_participant_types',
        sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_study_participant_types')),
    )
    op.add_column(
        'study_participants', sa.Column('study_participant_type_id', sa.UUID(), autoincrement=False, nullable=False)
    )
    op.create_foreign_key(
        op.f('fk_study_participants_study_participant_type_id'),
        'study_participants',
        'study_participant_types',
        ['study_participant_type_id'],
        ['id'],
    )

    op.create_table(
        'shuffled_movie_list_items',
        sa.Column('shuffle_list_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('movie_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('position', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
        sa.Column(
            'created_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column('deleted_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
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

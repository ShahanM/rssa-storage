"""Sync participant_movie_sequence tables with sqlalchemy models

Revision ID: fee2e90f5cf7
Revises: 6a98a185f3bb
Create Date: 2026-01-05 23:30:36.204889

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fee2e90f5cf7'
down_revision: str | None = '6a98a185f3bb'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'pre_shuffled_movie_lists', 'subset_desc', existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True
    )
    op.alter_column('pre_shuffled_movie_lists', 'seed', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        'pre_shuffled_movie_lists',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'pre_shuffled_movie_lists',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'pre_shuffled_movie_lists',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )
    op.add_column(
        'study_participant_movie_sessions',
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.add_column(
        'study_participant_movie_sessions', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.alter_column(
        'study_participant_movie_sessions',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'study_participant_movie_sessions',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.drop_constraint(
        op.f('fk_study_participant_movie_sessions_study_participant_id'),
        'study_participant_movie_sessions',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_movie_sessions_assigned_list_id'), 'study_participant_movie_sessions', type_='foreignkey'
    )
    op.create_foreign_key(
        op.f('fk_study_participant_movie_sessions_study_participant_id'),
        'study_participant_movie_sessions',
        'study_participants',
        ['study_participant_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f('fk_study_participant_movie_sessions_study_participant_id'),
        'study_participant_movie_sessions',
        type_='foreignkey',
    )
    op.create_foreign_key(
        op.f('fk_participant_movie_sessions_assigned_list_id'),
        'study_participant_movie_sessions',
        'pre_shuffled_movie_lists',
        ['assigned_list_id'],
        ['id'],
    )
    op.create_foreign_key(
        op.f('fk_study_participant_movie_sessions_study_participant_id'),
        'study_participant_movie_sessions',
        'study_participants',
        ['study_participant_id'],
        ['id'],
    )
    op.alter_column(
        'study_participant_movie_sessions',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'study_participant_movie_sessions', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False
    )
    op.drop_column('study_participant_movie_sessions', 'deleted_at')
    op.drop_column('study_participant_movie_sessions', 'updated_at')
    op.alter_column(
        'pre_shuffled_movie_lists',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    op.alter_column(
        'pre_shuffled_movie_lists',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'pre_shuffled_movie_lists', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False
    )
    op.alter_column('pre_shuffled_movie_lists', 'seed', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        'pre_shuffled_movie_lists', 'subset_desc', existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True
    )

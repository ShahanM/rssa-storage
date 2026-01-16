"""refactor pk/fks for the pre_shuffled_movies

Revision ID: 173182845d5d
Revises: bc6b5b4c9ef2
Create Date: 2025-11-07 00:54:56.411416

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '173182845d5d'
down_revision: str | None = 'bc6b5b4c9ef2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


PSL_PKEY_NAME = 'pre_shuffled_movie_lists_pkey'
PMS_PKEY_NAME = 'participant_movie_sessions_pkey'
PMS_ASSIGNED_LIST_FK_NAME = 'participant_movie_sessions_assigned_list_id_fkey'


def upgrade():
    op.drop_constraint(
        'participant_movie_sessions_assigned_list_id_fkey', 'participant_movie_sessions', type_='foreignkey'
    )

    op.alter_column('pre_shuffled_movie_lists', 'list_id', new_column_name='list_id_int_old')

    op.add_column('pre_shuffled_movie_lists', sa.Column('id', UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE pre_shuffled_movie_lists SET id = gen_random_uuid() WHERE id IS NULL')
    op.alter_column('pre_shuffled_movie_lists', 'id', nullable=False)

    op.drop_constraint('pre_shuffled_movie_lists_pkey', 'pre_shuffled_movie_lists', type_='primary')
    op.create_primary_key('pk_pre_shuffled_movie_lists', 'pre_shuffled_movie_lists', ['id'])

    op.add_column('participant_movie_sessions', sa.Column('id', UUID(as_uuid=True), nullable=True))
    op.execute('UPDATE participant_movie_sessions SET id = gen_random_uuid() WHERE id IS NULL')
    op.alter_column('participant_movie_sessions', 'id', nullable=False)

    op.drop_constraint('participant_movie_sessions_pkey', 'participant_movie_sessions', type_='primary')
    op.create_primary_key('pk_participant_movie_sessions', 'participant_movie_sessions', ['id'])

    op.create_foreign_key(
        'fk_participant_movie_sessions_participant_id',
        'participant_movie_sessions',
        'study_participants',
        ['participant_id'],
        ['id'],
    )

    op.add_column('participant_movie_sessions', sa.Column('assigned_list_id_uuid', UUID(as_uuid=True), nullable=True))
    op.execute("""
        UPDATE participant_movie_sessions AS pms
        SET assigned_list_id_uuid = psl.id
        FROM pre_shuffled_movie_lists AS psl
        WHERE pms.assigned_list_id = psl.list_id_int_old
    """)
    op.alter_column('participant_movie_sessions', 'assigned_list_id_uuid', nullable=False)
    op.drop_column('participant_movie_sessions', 'assigned_list_id')
    op.alter_column('participant_movie_sessions', 'assigned_list_id_uuid', new_column_name='assigned_list_id')

    op.create_foreign_key(
        'fk_participant_movie_sessions_assigned_list_id',
        'participant_movie_sessions',
        'pre_shuffled_movie_lists',
        ['assigned_list_id'],
        ['id'],
    )

    op.drop_column('pre_shuffled_movie_lists', 'list_id_int_old')


def downgrade():
    # Downgrading this is extremely complex and destructive.
    # It requires re-creating serials, re-linking, and dropping data.
    # It is strongly recommended to restore from backup instead.
    op.execute("RAISE EXCEPTION 'Downgrade not supported. Please restore from backup.'")
    # pass

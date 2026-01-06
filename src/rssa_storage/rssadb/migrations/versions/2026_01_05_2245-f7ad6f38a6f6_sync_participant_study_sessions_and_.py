"""Sync participant_study_sessions, and participant_recommendation_context tables with sqlalchemy models

Revision ID: f7ad6f38a6f6
Revises: 7c61de772826
Create Date: 2026-01-05 22:45:52.438158

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f7ad6f38a6f6'
down_revision: str | None = '7c61de772826'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'participant_recommendation_contexts',
        'recommendations_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        comment=None,
        existing_comment='\n            Stores the full list of generated recommendations, including ranks, IDs, and any predicted metrics.\n            ',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'study_step_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='\n            The specific step where the recommendation list was displayed. In situations where there are no pages.\n            ',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the recommendation list was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='A short name to identify the list type (e.g., Initial_List, Final_List_Shown).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.drop_constraint(
        op.f('uq_participant_recommendation_contexts'), 'participant_recommendation_contexts', type_='unique'
    )
    op.create_unique_constraint(
        op.f('uq_participant_recommendation_contexts_study_id_study_9290cf'),
        'participant_recommendation_contexts',
        ['study_id', 'study_participant_id', 'context_tag'],
    )
    op.add_column(
        'participant_study_sessions',
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.drop_constraint(op.f('uq_participant_study_sessions'), 'participant_study_sessions', type_='unique')


def downgrade() -> None:
    op.create_unique_constraint(
        op.f('uq_participant_study_sessions'),
        'participant_study_sessions',
        ['resume_code'],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column('participant_study_sessions', 'updated_at')
    op.drop_constraint(
        op.f('uq_participant_recommendation_contexts_study_id_study_9290cf'),
        'participant_recommendation_contexts',
        type_='unique',
    )
    op.create_unique_constraint(
        op.f('uq_participant_recommendation_contexts'),
        'participant_recommendation_contexts',
        ['study_id', 'study_participant_id', 'context_tag'],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("timezone('utc'::text, now())"),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("timezone('utc'::text, now())"),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment='A short name to identify the list type (e.g., Initial_List, Final_List_Shown).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the recommendation list was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'study_step_id',
        existing_type=sa.UUID(),
        comment='\n            The specific step where the recommendation list was displayed. In situations where there are no pages.\n            ',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'id',
        existing_type=sa.UUID(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'participant_recommendation_contexts',
        'recommendations_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        comment='\n            Stores the full list of generated recommendations, including ranks, IDs, and any predicted metrics.\n            ',
        existing_nullable=False,
    )

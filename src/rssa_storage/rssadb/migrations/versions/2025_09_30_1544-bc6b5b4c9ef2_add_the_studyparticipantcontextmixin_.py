"""add the StudyParticipantContextMixin columns to the rating and interactionLog

Revision ID: bc6b5b4c9ef2
Revises: b1f02a791be6
Create Date: 2025-09-30 15:44:16.833467

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = 'bc6b5b4c9ef2'
down_revision: str | None = 'b1f02a791be6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.rename_table('content_ratings', 'participant_ratings')
    op.execute('TRUNCATE TABLE participant_ratings CASCADE;')
    op.add_column(
        'participant_ratings',
        sa.Column(
            'study_id',
            UUID(as_uuid=True),
            sa.ForeignKey('studies.id'),
            nullable=False,
            comment='The specific study context.',
        ),
    )
    op.add_column(
        'participant_ratings',
        sa.Column(
            'step_id',
            UUID(as_uuid=True),
            sa.ForeignKey('study_steps.id'),
            nullable=False,
            comment='The specific study step context.',
        ),
    )
    op.add_column(
        'participant_ratings',
        sa.Column(
            'step_page_id',
            UUID(as_uuid=True),
            sa.ForeignKey('step_pages.id'),
            nullable=True,
            comment='The specific page where the content was displayed.',
        ),
    )
    op.add_column(
        'participant_ratings',
        sa.Column(
            'context_tag',
            sa.String(),
            nullable=False,
            comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        ),
    )
    op.add_column(
        'participant_ratings',
        sa.Column(
            'discarded',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('FALSE'),
            comment='Flag to discard record from analysis.',
        ),
    )
    op.create_unique_constraint(
        'uq_participant_ratings_item', 'participant_ratings', ['study_id', 'participant_id', 'item_id']
    )

    op.rename_table('interaction_logs', 'participant_interaction_logs')
    op.execute('TRUNCATE TABLE participant_interaction_logs CASCADE;')
    op.drop_column('participant_interaction_logs', 'action')
    op.drop_column('participant_interaction_logs', 'action_data')
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'study_id',
            UUID(as_uuid=True),
            sa.ForeignKey('studies.id'),
            nullable=False,
            comment='The specific study context.',
        ),
    )
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'step_id',
            UUID(as_uuid=True),
            sa.ForeignKey('study_steps.id'),
            nullable=False,
            comment='The specific study step context.',
        ),
    )
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'step_page_id',
            UUID(as_uuid=True),
            sa.ForeignKey('step_pages.id'),
            nullable=True,
            comment='The specific page where the content was displayed.',
        ),
    )
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'context_tag',
            sa.String(),
            nullable=False,
            comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        ),
    )
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'discarded',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('FALSE'),
            comment='Flag to discard record from analysis.',
        ),
    )
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'payload_json',
            JSONB,
            nullable=False,
            comment="""
            Stores the dynamic structured interaction payload (e.g., item clicks, hover duration, etc.).
            """,
        ),
    )
    op.add_column(
        'participant_interaction_logs',
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("TIMEZONE('utc', now())"),
            onupdate=sa.text("TIMEZONE('utc', now())"),
        ),
    )
    op.create_unique_constraint(
        'uq_interaction_context_tag', 'participant_interaction_logs', ['study_id', 'participant_id', 'context_tag']
    )


def downgrade() -> None:
    op.drop_constraint('uq_interaction_context_tag', 'participant_interaction_logs', type_='unique')
    op.drop_column('participant_interaction_logs', 'updated_at')
    op.drop_column('participant_interaction_logs', 'payload_json')
    op.drop_column('participant_interaction_logs', 'discarded')
    op.drop_column('participant_interaction_logs', 'context_tag')
    op.drop_column('participant_interaction_logs', 'step_page_id')
    op.drop_column('participant_interaction_logs', 'step_id')
    op.drop_column('participant_interaction_logs', 'study_id')

    op.add_column('participant_interaction_logs', sa.Column('action', sa.String(), nullable=True))
    op.add_column('participant_interaction_logs', sa.Column('action_data', sa.String(), nullable=True))

    op.rename_table('participant_interaction_logs', 'interaction_logs')

    op.drop_constraint('uq_participant_ratings_item', 'participant_ratings', type_='unique')
    op.drop_column('participant_ratings', 'discarded')
    op.drop_column('participant_ratings', 'context_tag')
    op.drop_column('participant_ratings', 'step_page_id')
    op.drop_column('participant_ratings', 'step_id')
    op.drop_column('participant_ratings', 'study_id')

    op.rename_table('participant_ratings', 'content_ratings')

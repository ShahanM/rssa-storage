"""add the StudyParticipantContextMixin columns

Revision ID: b1f02a791be6
Revises: 6958474f345c
Create Date: 2025-09-27 02:13:02.231866

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'b1f02a791be6'
down_revision: str | None = '6958474f345c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'feedbacks',
        sa.Column(
            'step_id',
            UUID(as_uuid=True),
            sa.ForeignKey('study_steps.id'),
            nullable=False,
            comment='The specific study step context.',
        ),
    )
    op.add_column(
        'feedbacks',
        sa.Column(
            'step_page_id',
            UUID(as_uuid=True),
            sa.ForeignKey('step_pages.id'),
            nullable=True,
            comment='The specific page where the content was displayed.',
        ),
    )
    op.add_column(
        'feedbacks',
        sa.Column(
            'context_tag',
            sa.String(),
            nullable=False,
            comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        ),
    )
    op.add_column(
        'feedbacks',
        sa.Column(
            'discarded',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('FALSE'),
            comment='Flag to discard record from analysis.',
        ),
    )
    op.create_unique_constraint('uq_feedbacks_context', 'feedbacks', ['study_id', 'participant_id', 'context_tag'])

    op.add_column(
        'survey_item_responses',
        sa.Column(
            'step_page_id',
            UUID(as_uuid=True),
            sa.ForeignKey('step_pages.id'),
            nullable=True,
            comment='The specific page where the survey was displayed.',
        ),
    )
    op.add_column(
        'survey_item_responses',
        sa.Column(
            'context_tag',
            sa.String(),
            nullable=False,
            comment='A short name to identify the survey context.',
        ),
    )
    op.create_unique_constraint('uq_survey_item', 'survey_item_responses', ['study_id', 'participant_id', 'item_id'])

    op.add_column(
        'freeform_responses',
        sa.Column(
            'step_page_id',
            UUID(as_uuid=True),
            sa.ForeignKey('step_pages.id'),
            nullable=True,
            comment='The specific page where the freeform input was located.',
        ),
    )
    op.create_unique_constraint(
        'uq_freeform_context', 'freeform_responses', ['study_id', 'participant_id', 'context_tag']
    )

    op.add_column(
        'study_interaction_responses',
        sa.Column(
            'step_id',
            UUID(as_uuid=True),
            sa.ForeignKey('study_steps.id'),
            nullable=False,
            comment='The specific study step context.',
        ),
    )
    op.add_column(
        'study_interaction_responses',
        sa.Column(
            'step_page_id',
            UUID(as_uuid=True),
            sa.ForeignKey('step_pages.id'),
            nullable=True,
            comment='The specific page where the interaction occurred.',
        ),
    )
    op.add_column(
        'study_interaction_responses',
        sa.Column(
            'discarded',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('FALSE'),
            comment='Flag to discard record from analysis.',
        ),
    )
    op.add_column('study_interaction_responses', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column(
        'participant_recommendation_context', sa.Column('version', sa.Integer(), nullable=False, server_default='1')
    )


def downgrade() -> None:
    op.drop_constraint('uq_freeform_context', 'freeform_responses', type_='unique')
    op.drop_constraint('uq_survey_item', 'survey_item_responses', type_='unique')
    op.drop_constraint('uq_feedbacks_context', 'feedbacks', type_='unique')

    # Participant Recommendation Context
    op.drop_column('participant_recommendation_context', 'version')

    # Study Interaction Responses
    op.drop_column('study_interaction_responses', 'version')
    op.drop_column('study_interaction_responses', 'discarded')
    op.drop_column('study_interaction_responses', 'step_page_id')
    op.drop_column('study_interaction_responses', 'step_id')

    # Freeform Responses
    op.drop_column('freeform_responses', 'step_page_id')

    # Survey Item Responses
    op.drop_column('survey_item_responses', 'context_tag')
    op.drop_column('survey_item_responses', 'step_page_id')

    # Feedbacks
    op.drop_column('feedbacks', 'discarded')
    op.drop_column('feedbacks', 'context_tag')
    op.drop_column('feedbacks', 'step_page_id')
    op.drop_column('feedbacks', 'step_id')

"""added index to some foreignkeys

Revision ID: 54fdaea3fde4
Revises: cdea8ad9c55b
Create Date: 2026-05-18 17:51:29.561132

"""

from collections.abc import Sequence

from alembic import op

revision: str = '54fdaea3fde4'
down_revision: str | None = 'cdea8ad9c55b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(op.f('ix_feedbacks_study_id'), 'feedbacks', ['study_id'], unique=False)
    op.create_index(op.f('ix_feedbacks_study_participant_id'), 'feedbacks', ['study_participant_id'], unique=False)
    op.create_index(op.f('ix_feedbacks_study_step_id'), 'feedbacks', ['study_step_id'], unique=False)
    op.create_index(op.f('ix_feedbacks_study_step_page_id'), 'feedbacks', ['study_step_page_id'], unique=False)
    op.create_index(
        op.f('ix_participant_attention_check_responses_study_id'),
        'participant_attention_check_responses',
        ['study_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_attention_check_responses_study_participant_id'),
        'participant_attention_check_responses',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_attention_check_responses_study_step_id'),
        'participant_attention_check_responses',
        ['study_step_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_attention_check_responses_study_step_page_id'),
        'participant_attention_check_responses',
        ['study_step_page_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_freeform_responses_study_id'), 'participant_freeform_responses', ['study_id'], unique=False
    )
    op.create_index(
        op.f('ix_participant_freeform_responses_study_participant_id'),
        'participant_freeform_responses',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_freeform_responses_study_step_id'),
        'participant_freeform_responses',
        ['study_step_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_freeform_responses_study_step_page_id'),
        'participant_freeform_responses',
        ['study_step_page_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_interaction_logs_study_id'), 'participant_interaction_logs', ['study_id'], unique=False
    )
    op.create_index(
        op.f('ix_participant_interaction_logs_study_participant_id'),
        'participant_interaction_logs',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_interaction_logs_study_step_id'),
        'participant_interaction_logs',
        ['study_step_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_interaction_logs_study_step_page_id'),
        'participant_interaction_logs',
        ['study_step_page_id'],
        unique=False,
    )
    op.create_index(op.f('ix_participant_ratings_study_id'), 'participant_ratings', ['study_id'], unique=False)
    op.create_index(
        op.f('ix_participant_ratings_study_participant_id'),
        'participant_ratings',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_ratings_study_step_id'), 'participant_ratings', ['study_step_id'], unique=False
    )
    op.create_index(
        op.f('ix_participant_ratings_study_step_page_id'), 'participant_ratings', ['study_step_page_id'], unique=False
    )
    op.create_index(
        op.f('ix_participant_recommendation_contexts_study_id'),
        'participant_recommendation_contexts',
        ['study_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_recommendation_contexts_study_participant_id'),
        'participant_recommendation_contexts',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_recommendation_contexts_study_step_id'),
        'participant_recommendation_contexts',
        ['study_step_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_recommendation_contexts_study_step_page_id'),
        'participant_recommendation_contexts',
        ['study_step_page_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_study_interaction_responses_study_id'),
        'participant_study_interaction_responses',
        ['study_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_study_interaction_responses_study_participant_id'),
        'participant_study_interaction_responses',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_study_interaction_responses_study_step_id'),
        'participant_study_interaction_responses',
        ['study_step_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_study_interaction_responses_study_step_page_id'),
        'participant_study_interaction_responses',
        ['study_step_page_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_survey_responses_study_id'), 'participant_survey_responses', ['study_id'], unique=False
    )
    op.create_index(
        op.f('ix_participant_survey_responses_study_participant_id'),
        'participant_survey_responses',
        ['study_participant_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_survey_responses_study_step_id'),
        'participant_survey_responses',
        ['study_step_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_participant_survey_responses_study_step_page_id'),
        'participant_survey_responses',
        ['study_step_page_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_participant_survey_responses_study_step_page_id'), table_name='participant_survey_responses')
    op.drop_index(op.f('ix_participant_survey_responses_study_step_id'), table_name='participant_survey_responses')
    op.drop_index(
        op.f('ix_participant_survey_responses_study_participant_id'), table_name='participant_survey_responses'
    )
    op.drop_index(op.f('ix_participant_survey_responses_study_id'), table_name='participant_survey_responses')
    op.drop_index(
        op.f('ix_participant_study_interaction_responses_study_step_page_id'),
        table_name='participant_study_interaction_responses',
    )
    op.drop_index(
        op.f('ix_participant_study_interaction_responses_study_step_id'),
        table_name='participant_study_interaction_responses',
    )
    op.drop_index(
        op.f('ix_participant_study_interaction_responses_study_participant_id'),
        table_name='participant_study_interaction_responses',
    )
    op.drop_index(
        op.f('ix_participant_study_interaction_responses_study_id'),
        table_name='participant_study_interaction_responses',
    )
    op.drop_index(
        op.f('ix_participant_recommendation_contexts_study_step_page_id'),
        table_name='participant_recommendation_contexts',
    )
    op.drop_index(
        op.f('ix_participant_recommendation_contexts_study_step_id'), table_name='participant_recommendation_contexts'
    )
    op.drop_index(
        op.f('ix_participant_recommendation_contexts_study_participant_id'),
        table_name='participant_recommendation_contexts',
    )
    op.drop_index(
        op.f('ix_participant_recommendation_contexts_study_id'), table_name='participant_recommendation_contexts'
    )
    op.drop_index(op.f('ix_participant_ratings_study_step_page_id'), table_name='participant_ratings')
    op.drop_index(op.f('ix_participant_ratings_study_step_id'), table_name='participant_ratings')
    op.drop_index(op.f('ix_participant_ratings_study_participant_id'), table_name='participant_ratings')
    op.drop_index(op.f('ix_participant_ratings_study_id'), table_name='participant_ratings')
    op.drop_index(op.f('ix_participant_interaction_logs_study_step_page_id'), table_name='participant_interaction_logs')
    op.drop_index(op.f('ix_participant_interaction_logs_study_step_id'), table_name='participant_interaction_logs')
    op.drop_index(
        op.f('ix_participant_interaction_logs_study_participant_id'), table_name='participant_interaction_logs'
    )
    op.drop_index(op.f('ix_participant_interaction_logs_study_id'), table_name='participant_interaction_logs')
    op.drop_index(
        op.f('ix_participant_freeform_responses_study_step_page_id'), table_name='participant_freeform_responses'
    )
    op.drop_index(op.f('ix_participant_freeform_responses_study_step_id'), table_name='participant_freeform_responses')
    op.drop_index(
        op.f('ix_participant_freeform_responses_study_participant_id'), table_name='participant_freeform_responses'
    )
    op.drop_index(op.f('ix_participant_freeform_responses_study_id'), table_name='participant_freeform_responses')
    op.drop_index(
        op.f('ix_participant_attention_check_responses_study_step_page_id'),
        table_name='participant_attention_check_responses',
    )
    op.drop_index(
        op.f('ix_participant_attention_check_responses_study_step_id'),
        table_name='participant_attention_check_responses',
    )
    op.drop_index(
        op.f('ix_participant_attention_check_responses_study_participant_id'),
        table_name='participant_attention_check_responses',
    )
    op.drop_index(
        op.f('ix_participant_attention_check_responses_study_id'), table_name='participant_attention_check_responses'
    )
    op.drop_index(op.f('ix_feedbacks_study_step_page_id'), table_name='feedbacks')
    op.drop_index(op.f('ix_feedbacks_study_step_id'), table_name='feedbacks')
    op.drop_index(op.f('ix_feedbacks_study_participant_id'), table_name='feedbacks')
    op.drop_index(op.f('ix_feedbacks_study_id'), table_name='feedbacks')

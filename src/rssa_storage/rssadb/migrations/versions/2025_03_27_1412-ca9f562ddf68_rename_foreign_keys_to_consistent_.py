"""Rename foreign keys to consistent naming convention

Revision ID: ca9f562ddf68
Revises: f7cad2259b6b
Create Date: 2025-03-27 14:12:11.855342

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ca9f562ddf68'
down_revision: str | None = 'f7cad2259b6b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint('study_participant_participant_type_fkey', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'fk_study_participant_participant_type_id',
        'study_participant',
        'participant_type',
        ['participant_type'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('study_participant_study_id_fkey', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'fk_study_participant_study_id', 'study_participant', 'study', ['study_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('study_participant_condition_id_fkey', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'fk_study_participant_study_condition_id',
        'study_participant',
        'study_condition',
        ['condition_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('study_participant_current_step_fkey', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'fk_study_participant_study_step_current_step',
        'study_participant',
        'study_step',
        ['current_step'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('study_participant_current_page_fkey', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'fk_study_participant_step_page_id',
        'study_participant',
        'step_page',
        ['current_page'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('participant_response_participant_id_fkey', 'participant_response', type_='foreignkey')
    op.create_foreign_key(
        'fk_participant_response_study_participant_id',
        'participant_response',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('participant_response_construct_id_fkey', 'participant_response', type_='foreignkey')
    op.create_foreign_key(
        'fk_participant_response_survey_construct_id',
        'participant_response',
        'survey_construct',
        ['construct_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('participant_response_item_id_fkey', 'participant_response', type_='foreignkey')
    op.create_foreign_key(
        'fk_participant_response_construct_item_id',
        'participant_response',
        'construct_item',
        ['item_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint(
        'participant_content_rating_participant_id_fkey', 'participant_content_rating', type_='foreignkey'
    )
    op.create_foreign_key(
        'fk_participant_content_rating_study_participant_id',
        'participant_content_rating',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('construct_item_construct_id_fkey', 'construct_item', type_='foreignkey')
    op.create_foreign_key(
        'fk_construct_item_survey_construct_id',
        'construct_item',
        'survey_construct',
        ['construct_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('construct_item_item_type_fkey', 'construct_item', type_='foreignkey')
    op.create_foreign_key(
        'fk_construct_item_construct_item_type_id',
        'construct_item',
        'construct_item_type',
        ['item_type'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('page_content_content_id_fkey', 'page_content', type_='foreignkey')
    op.create_foreign_key(
        'fk_page_content_survey_construct_id',
        'page_content',
        'survey_construct',
        ['content_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('page_content_page_id_fkey', 'page_content', type_='foreignkey')
    op.create_foreign_key(
        'fk_page_content_step_page_id', 'page_content', 'step_page', ['page_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('scale_level_scale_id_fkey', 'scale_level', type_='foreignkey')
    op.create_foreign_key(
        'fk_scale_level_construct_scale_id', 'scale_level', 'construct_scale', ['scale_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint(
        'participant_interaction_log_participant_id_fkey', 'participant_interaction_log', type_='foreignkey'
    )
    op.create_foreign_key(
        'fk_participant_interaction_log_study_participant_id',
        'participant_interaction_log',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('study_step_study_id_fkey', 'study_step', type_='foreignkey')
    op.create_foreign_key('fk_study_step_study_id', 'study_step', 'study', ['study_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('step_page_step_id_fkey', 'step_page', type_='foreignkey')
    op.create_foreign_key(
        'fk_step_page_study_step_id', 'step_page', 'study_step', ['step_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('step_page_study_id_fkey', 'step_page', type_='foreignkey')
    op.create_foreign_key('fk_step_page_study_id', 'step_page', 'study', ['study_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('study_condition_study_id_fkey', 'study_condition', type_='foreignkey')
    op.create_foreign_key(
        'fk_study_condition_study_id', 'study_condition', 'study', ['study_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('feedback_participant_id_fkey', 'feedback', type_='foreignkey')
    op.create_foreign_key(
        'fk_feedback_study_participant_id',
        'feedback',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('feedback_study_id_fkey', 'feedback', type_='foreignkey')
    op.create_foreign_key('fk_feedback_study_id', 'feedback', 'study', ['study_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('demographics_participant_id_fkey', 'demographics', type_='foreignkey')
    op.create_foreign_key(
        'fk_demographics_study_id', 'demographics', 'study_participant', ['participant_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('fk_survey_construct_type', 'survey_construct', type_='foreignkey')
    op.create_foreign_key(
        'fk_survey_construct_construct_type_id',
        'survey_construct',
        'construct_type',
        ['type'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('fk_survey_construct_scale', 'survey_construct', type_='foreignkey')
    op.create_foreign_key(
        'fk_survey_construct_construct_scale_id',
        'survey_construct',
        'construct_scale',
        ['scale'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint('fk_survey_construct_construct_scale_id', 'survey_construct', type_='foreignkey')
    op.create_foreign_key('fk_survey_construct_scale', 'survey_construct', 'construct_scale', ['scale'], ['id'])

    op.drop_constraint('fk_survey_construct_construct_type_id', 'survey_construct', type_='foreignkey')
    op.create_foreign_key('fk_survey_construct_type', 'survey_construct', 'construct_type', ['type'], ['id'])

    op.drop_constraint('fk_demographics_study_participant_id', 'demographics', type_='foreignkey')
    op.create_foreign_key(
        'demographics_participant_id_fkey', 'demographics', 'study_participant', ['participant_id'], ['id']
    )

    op.drop_constraint('fk_feedback_study_study_id', 'feedback', type_='foreignkey')
    op.create_foreign_key('feedback_study_id_fkey', 'feedback', 'study', ['study_id'], ['id'])

    op.drop_constraint('fk_feedback_study_participant_id', 'feedback', type_='foreignkey')
    op.create_foreign_key('feedback_participant_id_fkey', 'feedback', 'study_participant', ['participant_id'], ['id'])

    op.drop_constraint('fk_study_condition_study_id', 'study_condition', type_='foreignkey')
    op.create_foreign_key('study_condition_study_id_fkey', 'study_condition', 'study', ['study_id'], ['id'])

    op.drop_constraint('fk_step_page_study_id', 'step_page', type_='foreignkey')
    op.create_foreign_key('step_page_study_id_fkey', 'step_page', 'study', ['study_id'], ['id'])

    op.drop_constraint('fk_step_page_study_step_id', 'step_page', type_='foreignkey')
    op.create_foreign_key('step_page_step_id_fkey', 'step_page', 'study_step', ['step_id'], ['id'])

    op.drop_constraint('fk_study_step_study_study_id', 'study_step', type_='foreignkey')
    op.create_foreign_key('study_step_study_id_fkey', 'study_step', 'study', ['study_id'], ['id'])

    op.drop_constraint(
        'fk_participant_interaction_log_study_participant_id', 'participant_interaction_log', type_='foreignkey'
    )
    op.create_foreign_key(
        'participant_interaction_log_participant_id_fkey',
        'participant_interaction_log',
        'study_participant',
        ['participant_id'],
        ['id'],
    )

    op.drop_constraint('fk_scale_level_construct_scale_id', 'scale_level', type_='foreignkey')
    op.create_foreign_key('scale_level_scale_id_fkey', 'scale_level', 'scale', ['scale_id'], ['id'])

    op.drop_constraint('fk_page_content_step_page_id', 'page_content', type_='foreignkey')
    op.create_foreign_key('page_content_page_id_fkey', 'page_content', 'page', ['page_id'], ['id'])

    op.drop_constraint('fk_page_content_content_survey_construct_id', 'page_content', type_='foreignkey')
    op.create_foreign_key('page_content_content_id_fkey', 'page_content', 'survey_construct', ['content_id'], ['id'])

    op.drop_constraint('fk_construct_item_item_type_id', 'construct_item', type_='foreignkey')
    op.create_foreign_key('construct_item_item_type_fkey', 'construct_item', 'item_type', ['item_type'], ['id'])

    op.drop_constraint('fk_construct_item_survey_construct_id', 'construct_item', type_='foreignkey')
    op.create_foreign_key(
        'construct_item_construct_id_fkey', 'construct_item', 'survey_construct', ['construct_id'], ['id']
    )

    op.drop_constraint(
        'fk_participant_content_rating_study_participant_id', 'participant_content_rating', type_='foreignkey'
    )
    op.create_foreign_key(
        'participant_content_rating_participant_id_fkey',
        'participant_content_rating',
        'study_participant',
        ['participant_id'],
        ['id'],
    )

    op.drop_constraint('fk_participant_response_construct_item__id', 'participant_response', type_='foreignkey')
    op.create_foreign_key(
        'participant_response_item_id_fkey', 'participant_response', 'construct_item', ['item_id'], ['id']
    )

    op.drop_constraint('fk_participant_response_survey_construct_id', 'participant_response', type_='foreignkey')
    op.create_foreign_key(
        'participant_response_construct_id_fkey', 'participant_response', 'survey_construct', ['construct_id'], ['id']
    )

    op.drop_constraint('fk_participant_response_study_participant_id', 'participant_response', type_='foreignkey')
    op.create_foreign_key(
        'participant_response_participant_id_fkey',
        'participant_response',
        'study_participant',
        ['participant_id'],
        ['id'],
    )

    op.drop_constraint('fk_study_participant_study_step_current_step', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'study_participant_current_step_fkey', 'study_participant', 'study_step', ['current_step'], ['id']
    )

    op.drop_constraint('fk_study_participant_step_page_current_page', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'study_participant_current_page_fkey', 'study_participant', 'step_page', ['current_page'], ['id']
    )

    op.drop_constraint('fk_study_participant_study_condition_id', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'study_participant_condition_id_fkey', 'study_participant', 'study_condition', ['condition_id'], ['id']
    )

    op.drop_constraint('fk_study_participant_study_id', 'study_participant', type_='foreignkey')
    op.create_foreign_key('study_participant_study_id_fkey', 'study_participant', 'study', ['study_id'], ['id'])

    op.drop_constraint('fk_study_participant_participant_type_id', 'study_participant', type_='foreignkey')
    op.create_foreign_key(
        'study_participant_participant_type_fkey', 'study_participant', 'participant_type', ['participant_type'], ['id']
    )

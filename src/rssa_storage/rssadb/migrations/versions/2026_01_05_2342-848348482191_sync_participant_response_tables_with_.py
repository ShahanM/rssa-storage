"""Sync participant_response tables with sqlalchemy models

Revision ID: 848348482191
Revises: fee2e90f5cf7
Create Date: 2026-01-05 23:42:50.047807

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '848348482191'
down_revision: str | None = 'fee2e90f5cf7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        'feedbacks', 'id', existing_type=sa.UUID(), server_default=sa.text('gen_random_uuid()'), existing_nullable=False
    )
    op.alter_column(
        'feedbacks',
        'study_step_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'feedbacks',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the content was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'feedbacks',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        existing_nullable=False,
    )
    op.alter_column(
        'feedbacks',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment=None,
        existing_comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'feedbacks',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'feedbacks',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.drop_constraint(op.f('fk_feedbacks_study_id'), 'feedbacks', type_='foreignkey')
    op.drop_constraint(op.f('fk_feedbacks_study_step_page_id'), 'feedbacks', type_='foreignkey')
    op.drop_constraint(op.f('fk_feedbacks_study_participant_id'), 'feedbacks', type_='foreignkey')
    op.drop_constraint(op.f('fk_feedbacks_study_step_id'), 'feedbacks', type_='foreignkey')
    op.create_foreign_key(op.f('fk_feedbacks_study_id'), 'feedbacks', 'studies', ['study_id'], ['id'])
    op.create_foreign_key(op.f('fk_feedbacks_study_step_id'), 'feedbacks', 'study_steps', ['study_step_id'], ['id'])
    op.create_foreign_key(
        op.f('fk_feedbacks_study_participant_id'), 'feedbacks', 'study_participants', ['study_participant_id'], ['id']
    )
    op.create_foreign_key(
        op.f('fk_feedbacks_study_step_page_id'), 'feedbacks', 'study_step_pages', ['study_step_page_id'], ['id']
    )
    op.alter_column(
        'participant_freeform_responses',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_freeform_responses',
        'study_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='Foreign key to the study table',
        existing_nullable=False,
    )
    op.alter_column('participant_freeform_responses', 'study_step_id', existing_type=sa.UUID(), nullable=False)
    op.alter_column(
        'participant_freeform_responses',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the freeform input was located.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_freeform_responses', 'context_tag', existing_type=sa.TEXT(), type_=sa.String(), nullable=False
    )
    op.alter_column(
        'participant_freeform_responses',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_freeform_responses',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.drop_constraint(op.f('uq_participant_freeform_responses'), 'participant_freeform_responses', type_='unique')
    op.create_unique_constraint(
        op.f('uq_participant_freeform_responses_study_id_study_part_8006a1'),
        'participant_freeform_responses',
        ['study_id', 'study_participant_id', 'context_tag'],
    )
    op.add_column(
        'participant_interaction_logs', sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False)
    )
    op.alter_column(
        'participant_interaction_logs',
        'payload_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        comment=None,
        existing_comment='\n            Stores the dynamic structured interaction payload (e.g., item clicks, hover duration, etc.).\n            ',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'study_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific study context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'study_step_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the content was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_interaction_logs',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment=None,
        existing_comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'participant_interaction_logs',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_interaction_logs',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.drop_constraint(op.f('uq_participant_interaction_logs'), 'participant_interaction_logs', type_='unique')
    op.create_unique_constraint(
        op.f('uq_participant_interaction_logs_study_id_study_partic_6aa83f'),
        'participant_interaction_logs',
        ['study_id', 'study_participant_id', 'context_tag'],
    )
    op.alter_column(
        'participant_ratings',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'study_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific study context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'study_step_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the content was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_ratings',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment=None,
        existing_comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'participant_ratings',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_ratings',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'payload_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        comment=None,
        existing_comment='\n            Stores the dynamic structured response payload (e.g., chosen item ID, list rankings, predicted scores).\n            ',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'study_step_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the interaction occurred.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='A short name identifying the type of interaction (e.g., Final_Choice, Persona_Selection).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment=None,
        existing_comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.drop_constraint(
        op.f('uq_participant_study_interaction_responses'), 'participant_study_interaction_responses', type_='unique'
    )
    op.create_unique_constraint(
        op.f('uq_participant_study_interaction_responses_study_id_s_5834e0'),
        'participant_study_interaction_responses',
        ['study_id', 'study_participant_id', 'context_tag'],
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_step_page_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_participant_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_step_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_id'),
        'participant_study_interaction_responses',
        'studies',
        ['study_id'],
        ['id'],
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_step_page_id'),
        'participant_study_interaction_responses',
        'study_step_pages',
        ['study_step_page_id'],
        ['id'],
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_step_id'),
        'participant_study_interaction_responses',
        'study_steps',
        ['study_step_id'],
        ['id'],
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_participant_id'),
        'participant_study_interaction_responses',
        'study_participants',
        ['study_participant_id'],
        ['id'],
    )
    op.alter_column('participant_survey_responses', 'survey_item_id', existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        'participant_survey_responses',
        'survey_scale_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='Foreign key to the construct_scale table',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_survey_responses',
        'id',
        existing_type=sa.UUID(),
        server_default=sa.text('gen_random_uuid()'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses',
        'study_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='Foreign key to the study table',
        existing_nullable=False,
    )
    op.alter_column('participant_survey_responses', 'study_step_id', existing_type=sa.UUID(), nullable=False)
    op.alter_column(
        'participant_survey_responses',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment=None,
        existing_comment='The specific page where the survey was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_survey_responses',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment='A short name to identify the survey context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses',
        'discarded',
        existing_type=sa.BOOLEAN(),
        server_default=sa.text('FALSE'),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_survey_responses',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        existing_nullable=False,
    )
    op.drop_constraint(
        op.f('fk_participant_survey_responses_survey_item_id'), 'participant_survey_responses', type_='foreignkey'
    )
    op.drop_constraint(
        op.f('fk_participant_survey_responses_survey_scale_level_id'),
        'participant_survey_responses',
        type_='foreignkey',
    )
    op.create_foreign_key(
        op.f('fk_participant_survey_responses_survey_item_id'),
        'participant_survey_responses',
        'survey_items',
        ['survey_item_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        op.f('fk_participant_survey_responses_survey_scale_level_id'),
        'participant_survey_responses',
        'survey_scale_levels',
        ['survey_scale_level_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f('fk_participant_survey_responses_survey_scale_level_id'),
        'participant_survey_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_survey_responses_survey_item_id'), 'participant_survey_responses', type_='foreignkey'
    )
    op.create_foreign_key(
        op.f('fk_participant_survey_responses_survey_scale_level_id'),
        'participant_survey_responses',
        'survey_scale_levels',
        ['survey_scale_level_id'],
        ['id'],
    )
    op.create_foreign_key(
        op.f('fk_participant_survey_responses_survey_item_id'),
        'participant_survey_responses',
        'survey_items',
        ['survey_item_id'],
        ['id'],
    )
    op.alter_column(
        'participant_survey_responses',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_survey_responses',
        'discarded',
        existing_type=sa.BOOLEAN(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment='A short name to identify the survey context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the survey was displayed.',
        existing_nullable=True,
    )
    op.alter_column('participant_survey_responses', 'study_step_id', existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        'participant_survey_responses',
        'study_id',
        existing_type=sa.UUID(),
        comment='Foreign key to the study table',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_survey_responses', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False
    )
    op.alter_column(
        'participant_survey_responses',
        'survey_scale_id',
        existing_type=sa.UUID(),
        comment='Foreign key to the construct_scale table',
        existing_nullable=True,
    )
    op.alter_column('participant_survey_responses', 'survey_item_id', existing_type=sa.UUID(), nullable=False)
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_participant_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_step_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_step_page_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.drop_constraint(
        op.f('fk_participant_study_interaction_responses_study_id'),
        'participant_study_interaction_responses',
        type_='foreignkey',
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_step_id'),
        'participant_study_interaction_responses',
        'study_steps',
        ['study_step_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_id'),
        'participant_study_interaction_responses',
        'studies',
        ['study_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_participant_id'),
        'participant_study_interaction_responses',
        'study_participants',
        ['study_participant_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        op.f('fk_participant_study_interaction_responses_study_step_page_id'),
        'participant_study_interaction_responses',
        'study_step_pages',
        ['study_step_page_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.drop_constraint(
        op.f('uq_participant_study_interaction_responses_study_id_s_5834e0'),
        'participant_study_interaction_responses',
        type_='unique',
    )
    op.create_unique_constraint(
        op.f('uq_participant_study_interaction_responses'),
        'participant_study_interaction_responses',
        ['study_id', 'study_participant_id', 'context_tag'],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("timezone('utc'::text, now())"),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("timezone('utc'::text, now())"),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment='A short name identifying the type of interaction (e.g., Final_Choice, Persona_Selection).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the interaction occurred.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'study_step_id',
        existing_type=sa.UUID(),
        comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'id',
        existing_type=sa.UUID(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'participant_study_interaction_responses',
        'payload_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        comment='\nStores the dynamic structured response payload (e.g., chosen item ID, list rankings, predicted scores).\n',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        nullable=True,
    )
    op.alter_column(
        'participant_ratings',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_ratings',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'participant_ratings',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the content was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_ratings',
        'study_step_id',
        existing_type=sa.UUID(),
        comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_ratings',
        'study_id',
        existing_type=sa.UUID(),
        comment='The specific study context.',
        existing_nullable=False,
    )
    op.alter_column('participant_ratings', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)
    op.drop_constraint(
        op.f('uq_participant_interaction_logs_study_id_study_partic_6aa83f'),
        'participant_interaction_logs',
        type_='unique',
    )
    op.create_unique_constraint(
        op.f('uq_participant_interaction_logs'),
        'participant_interaction_logs',
        ['study_id', 'study_participant_id', 'context_tag'],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("timezone('utc'::text, now())"),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_interaction_logs',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'participant_interaction_logs',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the content was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'participant_interaction_logs',
        'study_step_id',
        existing_type=sa.UUID(),
        comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs',
        'study_id',
        existing_type=sa.UUID(),
        comment='The specific study context.',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_interaction_logs', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False
    )
    op.alter_column(
        'participant_interaction_logs',
        'payload_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        comment='\nStores the dynamic structured interaction payload (e.g., item clicks, hover duration, etc.).\n',
        existing_nullable=False,
    )
    op.drop_column('participant_interaction_logs', 'version')
    op.drop_constraint(
        op.f('uq_participant_freeform_responses_study_id_study_part_8006a1'),
        'participant_freeform_responses',
        type_='unique',
    )
    op.create_unique_constraint(
        op.f('uq_participant_freeform_responses'),
        'participant_freeform_responses',
        ['study_id', 'study_participant_id', 'context_tag'],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        'participant_freeform_responses',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("timezone('utc'::text, CURRENT_TIMESTAMP)"),
        existing_nullable=False,
    )
    op.alter_column(
        'participant_freeform_responses',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'participant_freeform_responses', 'context_tag', existing_type=sa.String(), type_=sa.TEXT(), nullable=True
    )
    op.alter_column(
        'participant_freeform_responses',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the freeform input was located.',
        existing_nullable=True,
    )
    op.alter_column('participant_freeform_responses', 'study_step_id', existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        'participant_freeform_responses',
        'study_id',
        existing_type=sa.UUID(),
        comment='Foreign key to the study table',
        existing_nullable=False,
    )
    op.alter_column(
        'participant_freeform_responses', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False
    )
    op.drop_constraint(op.f('fk_feedbacks_study_step_page_id'), 'feedbacks', type_='foreignkey')
    op.drop_constraint(op.f('fk_feedbacks_study_participant_id'), 'feedbacks', type_='foreignkey')
    op.drop_constraint(op.f('fk_feedbacks_study_step_id'), 'feedbacks', type_='foreignkey')
    op.drop_constraint(op.f('fk_feedbacks_study_id'), 'feedbacks', type_='foreignkey')
    op.create_foreign_key(
        op.f('fk_feedbacks_study_step_id'), 'feedbacks', 'study_steps', ['study_step_id'], ['id'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        op.f('fk_feedbacks_study_participant_id'),
        'feedbacks',
        'study_participants',
        ['study_participant_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        op.f('fk_feedbacks_study_step_page_id'),
        'feedbacks',
        'study_step_pages',
        ['study_step_page_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        op.f('fk_feedbacks_study_id'), 'feedbacks', 'studies', ['study_id'], ['id'], ondelete='CASCADE'
    )
    op.alter_column(
        'feedbacks',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        'feedbacks',
        'created_at',
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'feedbacks',
        'discarded',
        existing_type=sa.BOOLEAN(),
        comment='Flag to discard record from analysis.',
        existing_nullable=False,
        existing_server_default=sa.text('false'),
    )
    op.alter_column(
        'feedbacks',
        'context_tag',
        existing_type=sa.VARCHAR(),
        comment='A short name to identify the specific feedback context (e.g., Post_Intervention).',
        existing_nullable=False,
    )
    op.alter_column(
        'feedbacks',
        'study_step_page_id',
        existing_type=sa.UUID(),
        comment='The specific page where the content was displayed.',
        existing_nullable=True,
    )
    op.alter_column(
        'feedbacks',
        'study_step_id',
        existing_type=sa.UUID(),
        comment='The specific study step context.',
        existing_nullable=False,
    )
    op.alter_column('feedbacks', 'id', existing_type=sa.UUID(), server_default=None, existing_nullable=False)

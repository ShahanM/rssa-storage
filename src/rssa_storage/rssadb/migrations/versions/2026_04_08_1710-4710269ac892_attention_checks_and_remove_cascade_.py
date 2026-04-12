"""attention checks and remove cascade from participant responses

Revision ID: 4710269ac892
Revises: ac59e9e5273f
Create Date: 2026-04-08 17:10:08.660209

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '4710269ac892'
down_revision: str | None = 'ac59e9e5273f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'study_attention_checks',
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('assigned_position', sa.Integer(), nullable=False),
        sa.Column('study_step_id', sa.UUID(), nullable=False),
        sa.Column('study_step_page_id', sa.UUID(), nullable=False),
        sa.Column('study_step_page_content_id', sa.UUID(), nullable=False),
        sa.Column('survey_scale_id', sa.UUID(), nullable=False),
        sa.Column('expected_survey_scale_level_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['expected_survey_scale_level_id'],
            ['survey_scale_levels.id'],
            name=op.f('fk_study_attention_checks_expected_survey_scale_level_id'),
        ),
        sa.ForeignKeyConstraint(
            ['study_step_id'],
            ['study_steps.id'],
            name=op.f('fk_study_attention_checks_study_step_id'),
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['study_step_page_content_id'],
            ['study_step_page_contents.id'],
            name=op.f('fk_study_attention_checks_study_step_page_content_id'),
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['study_step_page_id'],
            ['study_step_pages.id'],
            name=op.f('fk_study_attention_checks_study_step_page_id'),
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['survey_scale_id'], ['survey_scales.id'], name=op.f('fk_study_attention_checks_survey_scale_id')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_study_attention_checks')),
    )
    op.create_table(
        'participant_attention_check_responses',
        sa.Column('study_attention_check_id', sa.UUID(), nullable=False),
        sa.Column('survey_scale_id', sa.UUID(), nullable=False),
        sa.Column('responded_survey_scale_level_id', sa.UUID(), nullable=True),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('study_id', sa.UUID(), nullable=False),
        sa.Column('study_step_id', sa.UUID(), nullable=False),
        sa.Column('study_step_page_id', sa.UUID(), nullable=True),
        sa.Column('study_participant_id', sa.UUID(), nullable=False),
        sa.Column('context_tag', sa.String(), nullable=False),
        sa.Column('version', sa.Integer(), server_default=sa.text('1'), nullable=False),
        sa.Column('discarded', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(
            ['responded_survey_scale_level_id'],
            ['survey_scale_levels.id'],
            name=op.f('fk_participant_attention_check_responses_responded_survey_scale_level_id'),
        ),
        sa.ForeignKeyConstraint(
            ['study_attention_check_id'],
            ['study_attention_checks.id'],
            name=op.f('fk_participant_attention_check_responses_study_attention_check_id'),
        ),
        sa.ForeignKeyConstraint(
            ['study_id'], ['studies.id'], name=op.f('fk_participant_attention_check_responses_study_id')
        ),
        sa.ForeignKeyConstraint(
            ['study_participant_id'],
            ['study_participants.id'],
            name=op.f('fk_participant_attention_check_responses_study_participant_id'),
        ),
        sa.ForeignKeyConstraint(
            ['study_step_id'], ['study_steps.id'], name=op.f('fk_participant_attention_check_responses_study_step_id')
        ),
        sa.ForeignKeyConstraint(
            ['study_step_page_id'],
            ['study_step_pages.id'],
            name=op.f('fk_participant_attention_check_responses_study_step_page_id'),
        ),
        sa.ForeignKeyConstraint(
            ['survey_scale_id'],
            ['survey_scales.id'],
            name=op.f('fk_participant_attention_check_responses_survey_scale_id'),
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_participant_attention_check_responses')),
    )


def downgrade() -> None:
    op.drop_table('participant_attention_check_responses')
    op.drop_table('study_attention_checks')

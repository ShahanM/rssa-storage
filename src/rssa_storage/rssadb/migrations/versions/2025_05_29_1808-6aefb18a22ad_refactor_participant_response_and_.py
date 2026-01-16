"""Refactor participant response and interaction tables

Revision ID: 6aefb18a22ad
Revises: dd1d4ec486f5
Create Date: 2025-05-29 18:08:00.933815

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = '6aefb18a22ad'
down_revision: str | None = 'dd1d4ec486f5'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Drop old index from participant_survey_response (old table)
    op.drop_constraint('participant_response_pkey', 'participant_survey_response', type_='primary')
    op.drop_index(
        'participant_response_construct_id_idx',
        table_name='participant_survey_response',
    )
    op.drop_index(
        'participant_response_participant_id_idx',
        table_name='participant_survey_response',
    )

    # Drop foreign keys on participant_survey_response
    op.drop_constraint(
        'fk_participant_survey_response_study_participant_id',
        'participant_survey_response',
        type_='foreignkey',
    )
    op.drop_constraint(
        'fk_participant_survey_response_survey_construct_id',
        'participant_survey_response',
        type_='foreignkey',
    )
    op.drop_constraint(
        'fk_participant_survey_response_construct_item_id',
        'participant_survey_response',
        type_='foreignkey',
    )

    # Drop foreign key on participant_content_rating
    op.drop_constraint(
        'fk_participant_content_rating_study_participant_id',
        'participant_content_rating',
        type_='foreignkey',
    )

    # Drop foreign key on participant_interaction_log
    op.drop_constraint(
        'fk_participant_interaction_log_study_participant_id',
        'participant_interaction_log',
        type_='foreignkey',
    )

    # Rename tables for more intuitive naming convention
    op.rename_table('participant_survey_response', 'survey_item_response')
    op.rename_table('participant_content_rating', 'content_rating')
    op.rename_table('participant_interaction_log', 'interaction_log')

    op.create_foreign_key(
        'fk_survey_item_response_study_participant_id',
        'survey_item_response',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.create_foreign_key(
        'fk_survey_item_response_survey_construct_id',
        'survey_item_response',
        'survey_construct',
        ['construct_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.create_foreign_key(
        'fk_survey_item_response_construct_item_id',
        'survey_item_response',
        'construct_item',
        ['item_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_content_rating_study_participant_id',
        'content_rating',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.create_foreign_key(
        'fk_interaction_log_study_participant_id',
        'interaction_log',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_table('participant_response')

    op.create_table(
        'freeform_response',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            default=lambda: uuid.uuid4(),
        ),
        sa.Column(
            'participant_id',
            UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            'step_id',
            UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            'item_id',
            UUID(as_uuid=True),
            sa.ForeignKey('construct_item.id'),
            nullable=True,
        ),
        sa.Column('context_tag', sa.String(length=50), nullable=True),
        sa.Column('response_text', sa.Text(), nullable=False),
        sa.Column(
            'date_created',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column(
            'date_modified',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column('discarded', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_foreign_key(
        'fk_freeform_response_study_participant_id',
        'freeform_response',
        'study_participant',
        ['participant_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_freeform_response_study_step_id',
        'freeform_response',
        'study_step',
        ['step_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_freeform_response_construct_item_id',
        'freeform_response',
        'construct_item',
        ['item_id'],
        ['id'],
    )

    with op.batch_alter_table('survey_item_response', schema=None) as batch_op:
        batch_op.add_column(sa.Column('step_id', UUID(as_uuid=True), nullable=True))
        batch_op.alter_column(
            'response',
            new_column_name='response_value',
            existing_type=sa.String(),
            nullable=False,
        )

    op.create_foreign_key(
        op.f('fk_survey_item_response_study_step_id'),
        'survey_item_response',
        'study_step',
        ['step_id'],
        ['id'],
    )

    # Ensure item_id and construct_id are non-nullable and have FKs
    with op.batch_alter_table('survey_item_response', schema=None) as batch_op:
        batch_op.alter_column('item_id', existing_type=UUID(as_uuid=True), nullable=False)
        batch_op.alter_column('construct_id', existing_type=UUID(as_uuid=True), nullable=False)

    op.alter_column(
        'content_rating',
        'date_created',
        type_=sa.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime,
    )

    with op.batch_alter_table('interaction_log', schema=None) as batch_op:
        batch_op.alter_column(
            'action_data',
            existing_type=sa.String(),
            type_=JSONB(),
            nullable=True,
        )
        batch_op.alter_column(
            'date_created',
            existing_type=sa.DateTime(),
            type_=sa.DateTime(timezone=True),
            nullable=False,
        )

    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column(
            'feedback',
            new_column_name='feedback_text',
            existing_type=sa.String(),
            nullable=False,
        )
        batch_op.alter_column(
            'created_at',
            existing_type=sa.DateTime(),
            type_=sa.DateTime(timezone=True),
            nullable=False,
        )
        batch_op.alter_column(
            'updated_at',
            existing_type=sa.DateTime(),
            type_=sa.DateTime(timezone=True),
            nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column(
            'updated_at',
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            nullable=False,
        )
        batch_op.alter_column(
            'created_at',
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            nullable=False,
        )
        batch_op.alter_column(
            'feedback_text',
            new_column_name='feedback',
            existing_type=sa.String(),
            nullable=False,
        )

    with op.batch_alter_table('interaction_log', schema=None) as batch_op:
        batch_op.alter_column(
            'date_created',
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            nullable=False,
        )
        batch_op.alter_column(
            'action_data',
            existing_type=JSONB(),
            type_=sa.String(),
            nullable=True,
        )

    op.alter_column(
        'content_rating',
        'date_created',
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.DateTime(),
    )

    with op.batch_alter_table('survey_item_response', schema=None) as batch_op:
        batch_op.drop_constraint(op.f('fk_survey_item_response_study_step_id'), type_='foreignkey')
        batch_op.drop_column('step_id')
        batch_op.alter_column(
            'response_value',
            new_column_name='response',
            existing_type=sa.String(),
            nullable=False,
        )

    op.drop_table('freeform_response')

    op.create_table(
        'participant_response',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            default=sa.text('gen_random_uuid()'),
        ),
        sa.Column('participant_id', UUID(as_uuid=True), nullable=False),
        sa.Column('step_id', UUID(as_uuid=True), nullable=False),
        sa.Column('response', JSONB(), nullable=False),
        sa.Column(
            'date_created',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column(
            'date_modified',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column('discarded', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_foreign_key(
        'fk_participant_response_study_participant_id',  # Use the exact original FK name
        'participant_response',
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'fk_participant_response_study_step_id',  # Use the exact original FK name
        'participant_response',
        'study_step',
        ['step_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.drop_constraint(
        'fk_interaction_log_study_participant_id',
        'interaction_log',
        type_='foreignkey',
    )
    op.drop_constraint(
        'fk_content_rating_study_participant_id',
        'content_rating',
        type_='foreignkey',
    )
    op.drop_constraint(
        'fk_survey_item_response_construct_item_id',
        'survey_item_response',
        type_='foreignkey',
    )
    op.drop_constraint(
        'fk_survey_item_response_survey_construct_id',
        'survey_item_response',
        type_='foreignkey',
    )
    op.drop_constraint(
        'fk_survey_item_response_study_participant_id',
        'survey_item_response',
        type_='foreignkey',
    )

    op.rename_table('interaction_log', 'participant_interaction_log')
    op.rename_table('content_rating', 'participant_content_rating')
    op.rename_table('survey_item_response', 'participant_survey_response')

    op.create_foreign_key(
        'fk_participant_interaction_log_study_participant_id',
        'participant_interaction_log',
        'study_participant',
        ['participant_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_participant_content_rating_study_participant_id',
        'participant_content_rating',
        'study_participant',
        ['participant_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_participant_survey_response_survey_construct_id',
        'participant_survey_response',
        'survey_construct',
        ['construct_id'],
        ['id'],
    )
    op.create_foreign_key(
        'fk_participant_survey_response_study_participant_id',
        'participant_survey_response',
        'study_participant',
        ['participant_id'],
        ['id'],
    )

    op.create_index(
        'participant_response_participant_id_idx',
        'participant_survey_response',
        ['participant_id'],
        unique=False,
    )
    op.create_index(
        'participant_response_construct_id_idx',
        'participant_survey_response',
        ['construct_id'],
        unique=False,
    )

    op.create_primary_key('participant_response_pkey', 'participant_survey_response', ['id'])

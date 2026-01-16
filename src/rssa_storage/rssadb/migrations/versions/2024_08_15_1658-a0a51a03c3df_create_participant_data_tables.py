"""create participant data tables

Revision ID: a0a51a03c3df
Revises: 2beaedbc6e85
Create Date: 2024-08-15 16:58:05.487980

"""

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'a0a51a03c3df'
down_revision: str | None = '2beaedbc6e85'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'participant_type',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('type', sa.String, nullable=False),
    )

    op.create_table(
        'study_participant',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('participant_type', UUID(as_uuid=True), nullable=False),
        sa.Column('external_id', sa.String, nullable=True),
        sa.Column('study_id', UUID(as_uuid=True), nullable=False),
        sa.Column('condition_id', UUID(as_uuid=True), nullable=False),
        sa.Column('current_status', sa.String, nullable=False),
        sa.Column('current_step', UUID(as_uuid=True), nullable=False),
        sa.Column('current_page', UUID(as_uuid=True), nullable=True),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.Column('date_updated', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.Column('discarded', sa.Boolean, nullable=False, default=False),
        sa.ForeignKeyConstraint(['participant_type'], ['participant_type.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['study_id'], ['study.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['condition_id'], ['study_condition.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['current_step'], ['study_step.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['current_page'], ['step_page.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'participant_response',
        sa.Column('participant_id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('construct_id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('item_id', UUID(as_uuid=True), nullable=True),
        sa.Column('response', sa.String, nullable=False),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.Column('discarded', sa.Boolean, nullable=False, default=False),
        sa.ForeignKeyConstraint(['participant_id'], ['study_participant.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['construct_id'], ['survey_construct.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['item_id'], ['construct_item.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'participant_content_rating',
        sa.Column('participant_id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('content_id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('content_type', sa.String, primary_key=True, nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('scale_min', sa.Integer, nullable=False),
        sa.Column('scale_max', sa.Integer, nullable=False),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.ForeignKeyConstraint(['participant_id'], ['study_participant.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'participant_interaction_log',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('participant_id', UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('action_data', sa.JSON, nullable=True),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.ForeignKeyConstraint(['participant_id'], ['study_participant.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('participant_interaction_log')
    op.drop_table('participant_content_rating')
    op.drop_table('participant_response')
    op.drop_table('study_participant')
    op.drop_table('participant_type')

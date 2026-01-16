"""create participant_response table for generic response logging

Revision ID: 2c5df8f6ec05
Revises: b751505559a7
Create Date: 2025-03-27 18:07:57.541692

"""

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = '2c5df8f6ec05'
down_revision: str | None = 'b751505559a7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


tablename = 'participant_response'
entity_study_participant_id = 'fk_participant_response_study_participant_id'
entity_study_step_id = 'fk_participant_response_study_step_id'


def upgrade() -> None:
    op.create_table(
        tablename,
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('participant_id', UUID(as_uuid=True), nullable=False),
        sa.Column('step_id', UUID(as_uuid=True), nullable=False),
        sa.Column('response', JSONB, nullable=False),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.Column('date_modified', sa.DateTime, nullable=False, default=datetime.now(UTC)),
        sa.Column('discarded', sa.Boolean, nullable=False, default=False),
    )

    # foreign key with study_participant
    op.create_foreign_key(
        entity_study_participant_id, tablename, 'study_participant', ['participant_id'], ['id'], ondelete='CASCADE'
    )

    # foreign key with study_step
    op.create_foreign_key(entity_study_step_id, tablename, 'study_step', ['step_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(entity_study_participant_id, tablename, type_='foreignkey')
    op.drop_constraint(entity_study_step_id, tablename, type_='foreignkey')
    op.drop_table(tablename)

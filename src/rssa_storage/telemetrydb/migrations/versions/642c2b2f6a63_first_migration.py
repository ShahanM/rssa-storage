"""first migration

Revision ID: 642c2b2f6a63
Revises:
Create Date: 2026-03-24 16:04:49.066106

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '642c2b2f6a63'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'participant_telemetry',
        sa.Column('participant_id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.UUID(), nullable=False),
        sa.Column('study_id', sa.UUID(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('item_id', sa.String(), nullable=True),
        sa.Column(
            'event_data', sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'), nullable=False
        ),
        sa.Column('client_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('server_timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_participant_telemetry')),
    )
    op.create_index(op.f('ix_participant_telemetry_event_type'), 'participant_telemetry', ['event_type'], unique=False)
    op.create_index(
        op.f('ix_participant_telemetry_participant_id'), 'participant_telemetry', ['participant_id'], unique=False
    )
    op.create_index(op.f('ix_participant_telemetry_session_id'), 'participant_telemetry', ['session_id'], unique=False)
    op.create_index(op.f('ix_participant_telemetry_study_id'), 'participant_telemetry', ['study_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_participant_telemetry_study_id'), table_name='participant_telemetry')
    op.drop_index(op.f('ix_participant_telemetry_session_id'), table_name='participant_telemetry')
    op.drop_index(op.f('ix_participant_telemetry_participant_id'), table_name='participant_telemetry')
    op.drop_index(op.f('ix_participant_telemetry_event_type'), table_name='participant_telemetry')
    op.drop_table('participant_telemetry')

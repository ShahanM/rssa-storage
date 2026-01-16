"""create feedback table

Revision ID: e702e5bd1477
Revises: 667aede70c01
Create Date: 2024-10-04 02:16:06.565756

"""

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'e702e5bd1477'
down_revision: str | None = '667aede70c01'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'feedback',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('participant_id', UUID(as_uuid=True), sa.ForeignKey('study_participant.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now(UTC)),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=datetime.now(UTC)),
        sa.Column('study_id', UUID(as_uuid=True), sa.ForeignKey('study.id'), nullable=False),
        sa.Column('feedback', sa.Text, nullable=False),
        sa.Column('feedback_type', sa.String, nullable=False),
        sa.Column('feedback_category', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('feedback')

"""create demographic table

Revision ID: 667aede70c01
Revises: c2172c2d0730
Create Date: 2024-10-03 19:05:40.735086

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '667aede70c01'
down_revision: Union[str, None] = 'c2172c2d0730'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('demographics',
        sa.Column('participant_id', UUID(as_uuid=True), sa.ForeignKey('study_participant.id'), primary_key=True),
        sa.Column('age_range', sa.String(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('gender_other', sa.String(), nullable=True),
        sa.Column('race', sa.String(), nullable=False),
        sa.Column('race_other', sa.String(), nullable=True),
        sa.Column('education', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('state_region', sa.String(), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)),
        sa.Column('date_updated', sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)),
        sa.Column('discarded', sa.Boolean(), nullable=False, default=False),
    )


def downgrade() -> None:
    op.drop_table('demographics')


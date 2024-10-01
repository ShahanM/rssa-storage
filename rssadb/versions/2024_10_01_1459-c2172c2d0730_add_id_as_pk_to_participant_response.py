"""add id as pk to participant response

Revision ID: c2172c2d0730
Revises: 9ed2a79b1c93
Create Date: 2024-10-01 14:59:43.970733

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2172c2d0730'
down_revision: Union[str, None] = '9ed2a79b1c93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('participant_response_pkey', 'participant_response', type_='primary')
    op.add_column('participant_response', sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4))
    op.add_column('participant_response', sa.Column('date_modified', sa.DateTime, nullable=False, default=datetime.now(timezone.utc)))
    op.create_index('participant_response_participant_id_idx', 'participant_response', ['participant_id'])
    op.create_index('participant_response_construct_id_idx', 'participant_response', ['construct_id'])
    op.create_primary_key('participant_response_pkey', 'participant_response', ['id', 'participant_id', 'construct_id'])


def downgrade() -> None:
    op.drop_constraint('participant_response_pkey', 'participant_response', type_='primary')
    op.drop_index('participant_response_construct_id_idx', table_name='participant_response')
    op.drop_index('participant_response_participant_id_idx', table_name='participant_response')
    op.drop_column('participant_response', 'id')
    op.drop_column('participant_response', 'date_modified')


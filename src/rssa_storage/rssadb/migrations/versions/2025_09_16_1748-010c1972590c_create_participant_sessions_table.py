"""create participant_sessions table

Revision ID: 010c1972590c
Revises: e16e67f2f146
Create Date: 2025-09-16 17:48:28.515911

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '010c1972590c'
down_revision: Union[str, None] = 'e16e67f2f146'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		'participant_sessions',
		sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
		sa.Column('participant_id', UUID(as_uuid=True), sa.ForeignKey('study_participants.id'), nullable=False),
		sa.Column('resume_code', sa.String(length=5), nullable=False, unique=True),
		sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
		sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
		sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
	)


def downgrade() -> None:
	op.drop_table('participant_sessions')

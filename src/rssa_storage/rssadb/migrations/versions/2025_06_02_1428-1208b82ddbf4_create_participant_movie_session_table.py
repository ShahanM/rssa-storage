"""create participant movie session table

Revision ID: 1208b82ddbf4
Revises: 27aeaf12b4d4
Create Date: 2025-06-02 14:28:15.231601

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '1208b82ddbf4'
down_revision: Union[str, None] = '27aeaf12b4d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		'participant_movie_sessions',
		sa.Column('participant_id', UUID(as_uuid=True), primary_key=True),
		sa.Column(
			'assigned_list_id',
			sa.Integer(),
			sa.ForeignKey('pre_shuffled_movie_lists.list_id'),
			nullable=False,
		),
		sa.Column('current_offset', sa.Integer(), server_default='0', nullable=False),
		sa.Column(
			'created_at',
			sa.DateTime(timezone=True),
			server_default=sa.text('now()'),
			nullable=False,
		),
		sa.Column(
			'last_accessed_at',
			sa.DateTime(timezone=True),
			server_default=sa.text('now()'),
			nullable=False,
		),
	)


def downgrade() -> None:
	op.drop_table('participant_movie_sessions')

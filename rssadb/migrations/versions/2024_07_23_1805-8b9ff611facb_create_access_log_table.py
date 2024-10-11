"""Create access log table

Revision ID: 8b9ff611facb
Revises: accaafd84165
Create Date: 2024-07-23 18:05:32.191751

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b9ff611facb'
down_revision: Union[str, None] = 'accaafd84165'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('access_log',
        sa.Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True),
        sa.Column('auth0_user', sa.String, nullable=False),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('resource', sa.String, nullable=False),
        sa.Column('resource_id', sa.String, nullable=True),
        sa.Column('timestamp', sa.DateTime, nullable=False, default=datetime.now(timezone.utc))
    )

def downgrade() -> None:
    op.drop_table('access_log')

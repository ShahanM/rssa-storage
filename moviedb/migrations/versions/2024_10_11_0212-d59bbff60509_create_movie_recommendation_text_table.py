"""create movie recommendation text table

Revision ID: d59bbff60509
Revises: 25c5cdf9ee9c
Create Date: 2024-10-11 02:12:40.391591

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd59bbff60509'
down_revision: Union[str, None] = '25c5cdf9ee9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'movie_recommendation_text',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('movie_id', UUID(as_uuid=True), nullable=False),
        sa.Column('formal', sa.Text, nullable=False),
        sa.Column('informal', sa.Text, nullable=False),

        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    )

    op.create_index('movie_recommendation_text_id_idx', 'movie_recommendation_text', ['movie_id'], unique=True)
    op.create_foreign_key('movie_id_fk', 'movie_recommendation_text', 'movies', ['movie_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('movie_id_fk', 'movie_recommendation_text')
    op.drop_index('movie_recommendation_text_id_idx')
    op.drop_table('movie_recommendation_text')

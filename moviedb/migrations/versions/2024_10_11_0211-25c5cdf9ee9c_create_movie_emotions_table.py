"""create movie emotions table



Revision ID: 25c5cdf9ee9c
Revises: a5acb0321e2e
Create Date: 2024-10-11 02:11:53.846911

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25c5cdf9ee9c'
down_revision: Union[str, None] = 'a5acb0321e2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'movie_emotions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('movie_id', UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('movielens_id', sa.String, nullable=False),
        sa.Column('anger', sa.Numeric, nullable=False),
        sa.Column('anticipation', sa.Numeric, nullable=False),
        sa.Column('disgust', sa.Numeric, nullable=False),
        sa.Column('fear', sa.Numeric, nullable=False),
        sa.Column('joy', sa.Numeric, nullable=False),
        sa.Column('surprise', sa.Numeric, nullable=False),
        sa.Column('sadness', sa.Numeric, nullable=False),
        sa.Column('trust', sa.Numeric, nullable=False)
    )

    op.create_index('movielens_emotions_id_idx', 'movie_emotions', ['movielens_id'], unique=True)
    op.create_foreign_key('movie_id_fk', 'movie_emotions', 'movies', ['movie_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('movie_id_fk', 'movie_emotions')
    op.drop_index('movielens_emotions_id_idx')
    op.drop_table('movie_emotions')

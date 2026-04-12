"""made all demographics nullable and added urbanicity

Revision ID: a12e2fa9a176
Revises: 4710269ac892
Create Date: 2026-04-09 18:33:03.603570

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = 'a12e2fa9a176'
down_revision: str | None = '4710269ac892'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('participant_demographics', sa.Column('urbanicity', sa.String(), nullable=True))
    op.add_column(
        'participant_demographics', sa.Column('raw_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False)
    )
    op.alter_column('participant_demographics', 'age_range', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('participant_demographics', 'gender', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('participant_demographics', 'race', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('participant_demographics', 'education', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column('participant_demographics', 'country', existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    op.alter_column('participant_demographics', 'country', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('participant_demographics', 'education', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('participant_demographics', 'race', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('participant_demographics', 'gender', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('participant_demographics', 'age_range', existing_type=sa.VARCHAR(), nullable=False)
    op.drop_column('participant_demographics', 'raw_json')
    op.drop_column('participant_demographics', 'urbanicity')

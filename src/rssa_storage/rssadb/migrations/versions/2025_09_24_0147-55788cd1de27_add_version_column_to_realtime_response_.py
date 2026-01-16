"""add version column to realtime response tables

Revision ID: 55788cd1de27
Revises: 77c4ea61cb82
Create Date: 2025-09-24 01:47:10.866322

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '55788cd1de27'
down_revision: str | None = '77c4ea61cb82'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('demographics', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('feedbacks', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('survey_item_responses', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('freeform_responses', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('content_ratings', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))


def downgrade() -> None:
    op.drop_column('content_ratings', 'version')
    op.drop_column('freeform_responses', 'version')
    op.drop_column('survey_item_responses', 'version')
    op.drop_column('feedbacks', 'version')
    op.drop_column('demographics', 'version')

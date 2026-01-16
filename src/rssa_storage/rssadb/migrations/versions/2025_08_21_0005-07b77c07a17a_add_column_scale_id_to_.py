"""add column scale_id to SurveyItemResponse

Revision ID: 07b77c07a17a
Revises: 0a7f9a5a38bc
Create Date: 2025-08-21 00:05:37.250905

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '07b77c07a17a'
down_revision: str | None = '0a7f9a5a38bc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'survey_item_response',
        sa.Column(
            'scale_id',
            UUID(as_uuid=True),
            nullable=True,
            comment='Foreign key to the construct_scale table',
        ),
    )

    op.create_foreign_key(
        op.f('fk_survey_item_response_construct_scale_id'),
        'survey_item_response',
        'construct_scale',
        ['scale_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint(op.f('fk_survey_item_response_construct_scale_id'), 'survey_item_response', type_='foreignkey')
    op.drop_column('survey_item_response', 'scale_id')

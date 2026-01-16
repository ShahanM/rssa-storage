"""remove unique constraint from survey response, and ratings

Revision ID: 08a92578f639
Revises: 5af952aa36e6
Create Date: 2025-12-12 09:08:51.095731

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '08a92578f639'
down_revision: str | None = '5af952aa36e6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint('uq_participant_survey_responses', 'participant_survey_responses', type_='unique')
    op.drop_constraint('uq_participant_ratings', 'participant_ratings', type_='unique')


def downgrade() -> None:
    op.create_unique_constraint(
        'uq_participant_survey_responses',
        'participant_survey_responses',
        ['study_participant_id', 'study_step_page_id', 'study_step_id', 'study_id'],
    )
    op.create_unique_constraint(
        'uq_participant_ratings',
        'participant_ratings',
        ['study_participant_id', 'study_step_page_id', 'study_step_id', 'study_id'],
    )

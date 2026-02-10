"""Add a authorized_test_code field to the study_conditions.

RATIONALE: The authorized_test_code would allow specifying a fixed condition when testing studies.

SIDE EFFECT NOTE: We are also dropping the unique constraint uq_participant_ratings. This was
added to the model without updating the migrations.

RATIONALE: uq_participant_ratings constraints one rating per participant per study. It is more
realistic to limit one rating per participant per study_step, or study_step_page. For now, we
handle the required uniqueness at the API service validation stage.

Revision ID: 7ab04095d69b
Revises: 5deb4502edb4
Create Date: 2026-02-10 12:46:30.112254

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7ab04095d69b'
down_revision: str | None = '5deb4502edb4'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('study_conditions', sa.Column('authorized_test_code', sa.String(length=16), nullable=True))

    # The side effect mentioned in the preamble.
    op.drop_constraint(op.f('uq_participant_ratings'), 'participant_ratings', type_='unique')


def downgrade() -> None:
    op.create_unique_constraint(
        op.f('uq_participant_ratings'),
        'participant_ratings',
        ['study_id', 'study_participant_id', 'item_id'],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column('study_conditions', 'authorized_test_code')

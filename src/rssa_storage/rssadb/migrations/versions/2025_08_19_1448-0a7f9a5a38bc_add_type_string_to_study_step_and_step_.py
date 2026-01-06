"""add type string to study_step, and step_page to differentiate surveys

Revision ID: 0a7f9a5a38bc
Revises: 6257cf839b1a
Create Date: 2025-08-19 14:48:04.589714

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0a7f9a5a38bc'
down_revision: Union[str, None] = '6257cf839b1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# Add type column to study_step
	op.add_column(
		'study_step',
		sa.Column(
			'step_type',
			sa.String(),
			nullable=True,
			comment='Type of step - "survey", "preference-elicitation", "study-information",'
			+ '"interaction", and "demographics',
		),
	)

	# Add type column to step_page
	op.add_column(
		'step_page',
		sa.Column(
			'page_type',
			sa.String(),
			nullable=True,
			comment='Type of page, e.g.,' + '"survey" or "null" for non-survey pages',
		),
	)


def downgrade() -> None:
	op.drop_column('step_page', 'step_type')
	op.drop_column('study_step', 'page_type')

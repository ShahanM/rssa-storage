"""add study_id fk columns to response tables

Revision ID: 6912b533545a
Revises: dab1b0751432
Create Date: 2025-07-03 14:37:54.537648

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '6912b533545a'
down_revision: Union[str, None] = 'dab1b0751432'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column(
		'survey_item_response',
		sa.Column(
			'study_id',
			UUID(as_uuid=True),
			nullable=True,  # This is nullable now to accomodate existing records
			comment='Foreign key to the study table',
		),
	)

	op.execute(
		"""
        UPDATE survey_item_response sir
        SET study_id = sp.study_id
        FROM study_participant sp
        WHERE sir.participant_id = sp.id;
        """
	)

	op.alter_column(
		'survey_item_response',
		'study_id',
		existing_type=UUID(as_uuid=True),
		nullable=False,
		comment='Foreign key to the study table',
	)

	op.create_foreign_key(
		op.f('fk_survey_item_response_study_study_id'),
		'survey_item_response',
		'study',
		['study_id'],
		['id'],
		ondelete='CASCADE',
	)

	op.add_column(
		'freeform_response',
		sa.Column(
			'study_id',
			UUID(as_uuid=True),
			nullable=True,
			comment='Foreign key to the study table',
		),
	)

	op.execute(
		"""
        UPDATE freeform_response fr
        SET study_id = sp.study_id
        FROM study_participant sp
        WHERE fr.participant_id = sp.id;
        """
	)

	op.alter_column(
		'freeform_response',
		'study_id',
		existing_type=UUID(as_uuid=True),
		nullable=False,
		comment='Foreign key to the study table',
	)

	op.create_foreign_key(
		op.f('fk_freeform_response_study_study_id'),
		'freeform_response',
		'study',
		['study_id'],
		['id'],
		ondelete='CASCADE',
	)


def downgrade() -> None:
	op.drop_constraint(
		op.f('fk_freeform_response_study_study_id'),
		'freeform_response',
		type_='foreignkey',
	)
	op.drop_column('freeform_response', 'study_id')

	op.drop_constraint(
		op.f('fk_survey_item_response_study_study_id'),
		'survey_item_response',
		type_='foreignkey',
	)
	op.drop_column('survey_item_response', 'study_id')

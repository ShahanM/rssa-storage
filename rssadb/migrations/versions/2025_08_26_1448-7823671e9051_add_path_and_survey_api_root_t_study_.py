"""Add path and survey_api_root to study_step table

Revision ID: 7823671e9051
Revises: 07b77c07a17a
Create Date: 2025-08-26 14:48:11.701373

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7823671e9051'
down_revision: Union[str, None] = '07b77c07a17a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column(
		'study_step',
		sa.Column('path', sa.String(), nullable=True),
	)

	study_step_table = sa.table(
		'study_step',
		sa.column('id', sa.dialects.postgresql.UUID),
		sa.column('title', sa.String),
		sa.column('path', sa.String),
	)

	slugified_path = sa.func.concat(
		'/',
		sa.func.lower(sa.func.replace(study_step_table.c.title, ' ', '-')),
		'-',
		sa.cast(study_step_table.c.id, sa.String),  # Cast UUID to string for concatenation
	)

	op.execute(study_step_table.update().where(study_step_table.c.path.is_(None)).values(path=slugified_path))

	op.alter_column('study_step', 'path', nullable=False)

	op.add_column('study_step', sa.Column('survey_api_root', sa.String(), nullable=True))

	op.create_unique_constraint(
		'uq_study_step_study_id_path',
		'study_step',
		['study_id', 'path'],
	)


def downgrade() -> None:
	op.drop_constraint('uq_study_step_study_id_path', 'study_step', type_='unique')

	op.drop_column('study_step', 'survey_api_root')
	op.drop_column('study_step', 'path')

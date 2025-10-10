"""Add ON DELETE CASCADE to foreign keys

Revision ID: f7cad2259b6b
Revises: 64e9eabe86b9
Create Date: 2025-02-21 17:34:37.764378

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f7cad2259b6b'
down_revision: Union[str, None] = '64e9eabe86b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.drop_constraint('study_step_study_id_fkey', 'study_step', type_='foreignkey')
	op.create_foreign_key('study_step_study_id_fkey', 'study_step', 'study', ['study_id'], ['id'], ondelete='CASCADE')

	op.drop_constraint('step_page_step_id_fkey', 'step_page', type_='foreignkey')
	op.create_foreign_key('step_page_step_id_fkey', 'step_page', 'study_step', ['step_id'], ['id'], ondelete='CASCADE')

	op.drop_constraint('step_page_study_id_fkey', 'step_page', type_='foreignkey')
	op.create_foreign_key('step_page_study_id_fkey', 'step_page', 'study', ['study_id'], ['id'], ondelete='CASCADE')

	op.drop_constraint('study_condition_study_id_fkey', 'study_condition', type_='foreignkey')
	op.create_foreign_key(
		'study_condition_study_id_fkey', 'study_condition', 'study', ['study_id'], ['id'], ondelete='CASCADE'
	)

	op.drop_constraint('feedback_participant_id_fkey', 'feedback', type_='foreignkey')
	op.create_foreign_key(
		'feedback_participant_id_fkey', 'feedback', 'study_participant', ['participant_id'], ['id'], ondelete='CASCADE'
	)

	op.drop_constraint('feedback_study_id_fkey', 'feedback', type_='foreignkey')
	op.create_foreign_key('feedback_study_id_fkey', 'feedback', 'study', ['study_id'], ['id'], ondelete='CASCADE')

	op.drop_constraint('demographics_participant_id_fkey', 'demographics', type_='foreignkey')
	op.create_foreign_key(
		'demographics_participant_id_fkey',
		'demographics',
		'study_participant',
		['participant_id'],
		['id'],
		ondelete='CASCADE',
	)


def downgrade() -> None:
	op.drop_constraint('demographics_participant_id_fkey', 'demographics', type_='foreignkey')
	op.create_foreign_key(
		'demographics_participant_id_fkey', 'demographics', 'study_participant', ['participant_id'], ['id']
	)

	op.drop_constraint('feedback_study_id_fkey', 'feedback', type_='foreignkey')
	op.create_foreign_key('feedback_study_id_fkey', 'feedback', 'study', ['study_id'], ['id'])

	op.drop_constraint('feedback_participant_id_fkey', 'feedback', type_='foreignkey')
	op.create_foreign_key('feedback_participant_id_fkey', 'feedback', 'study_participant', ['participant_id'], ['id'])

	op.drop_constraint('study_condition_study_id_fkey', 'study_condition', type_='foreignkey')
	op.create_foreign_key('study_condition_study_id_fkey', 'study_condition', 'study', ['study_id'], ['id'])

	op.drop_constraint('step_page_study_id_fkey', 'step_page', type_='foreignkey')
	op.create_foreign_key('step_page_study_id_fkey', 'step_page', 'study', ['study_id'], ['id'])

	op.drop_constraint('step_page_step_id_fkey', 'step_page', type_='foreignkey')
	op.create_foreign_key('step_page_step_id_fkey', 'step_page', 'study_step', ['step_id'], ['id'])

	op.drop_constraint('study_step_study_id_fkey', 'study_step', type_='foreignkey')
	op.create_foreign_key('study_step_study_id_fkey', 'study_step', 'study', ['study_id'], ['id'])

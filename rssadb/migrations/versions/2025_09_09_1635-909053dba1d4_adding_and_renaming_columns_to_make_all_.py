"""adding and renaming columns to make all tables consistent

Revision ID: 909053dba1d4
Revises: 37940c469741
Create Date: 2025-09-09 16:35:37.039795

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '909053dba1d4'
down_revision: Union[str, None] = '37940c469741'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# ### ConstructItems ###
	op.rename_table('construct_item', 'construct_items')
	op.add_column('construct_items', sa.Column('notes', sa.String(), nullable=True))
	op.add_column('construct_items', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('construct_items', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('construct_items', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('construct_items', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key(
		'fk_construct_items_created_by_id_users', 'construct_items', 'users', ['created_by_id'], ['id']
	)

	# ### SurveyConstructs ###
	op.rename_table('survey_construct', 'survey_constructs')
	op.alter_column('survey_constructs', 'desc', new_column_name='description')
	op.add_column('survey_constructs', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('survey_constructs', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('survey_constructs', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('survey_constructs', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key(
		'fk_survey_constructs_created_by_id_users', 'survey_constructs', 'users', ['created_by_id'], ['id']
	)

	# ### ConstructScales ###
	op.rename_table('construct_scale', 'construct_scales')
	op.drop_column('construct_scales', 'created_by')
	op.add_column('construct_scales', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('construct_scales', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('construct_scales', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('construct_scales', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key(
		'fk_construct_scales_created_by_id_users', 'construct_scales', 'users', ['created_by_id'], ['id']
	)

	# ### ScaleLevels ###
	op.rename_table('scale_level', 'scale_levels')
	op.add_column('scale_levels', sa.Column('notes', sa.String(), nullable=True))
	op.add_column('scale_levels', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('scale_levels', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('scale_levels', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('scale_levels', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key('fk_scale_levels_created_by_id_users', 'scale_levels', 'users', ['created_by_id'], ['id'])

	# ### Studies ###
	op.rename_table('study', 'studies')
	op.alter_column('studies', 'date_created', new_column_name='created_at')
	op.add_column('studies', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('studies', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

	# ### StudyConditions ###
	op.rename_table('study_condition', 'study_conditions')
	op.alter_column('study_conditions', 'date_created', new_column_name='created_at')
	op.add_column('study_conditions', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('study_conditions', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('study_conditions', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key(
		'fk_study_conditions_created_by_id_users', 'study_conditions', 'users', ['created_by_id'], ['id']
	)

	# ### StudySteps ###
	op.rename_table('study_step', 'study_steps')
	op.alter_column('study_steps', 'date_created', new_column_name='created_at')
	op.add_column('study_steps', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('study_steps', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('study_steps', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key('fk_study_steps_created_by_id_users', 'study_steps', 'users', ['created_by_id'], ['id'])

	# ### Pages ###
	op.rename_table('step_page', 'step_pages')
	op.alter_column('step_pages', 'date_created', new_column_name='created_at')
	op.add_column('step_pages', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('step_pages', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('step_pages', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key('fk_step_pages_created_by_id_users', 'step_pages', 'users', ['created_by_id'], ['id'])

	# ### PageContents ###
	op.rename_table('page_content', 'page_contents')
	op.alter_column('page_contents', 'content_id', new_column_name='construct_id')
	op.add_column('page_contents', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('page_contents', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('page_contents', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('page_contents', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
	op.create_foreign_key('fk_page_contents_created_by_id_users', 'page_contents', 'users', ['created_by_id'], ['id'])

	# ### SurveyItemResponse ###
	op.rename_table('survey_item_response', 'survey_item_responses')
	op.alter_column('survey_item_responses', 'response', new_column_name='scale_level_id')
	op.alter_column('survey_item_responses', 'date_created', new_column_name='created_at')
	op.alter_column('survey_item_responses', 'date_modified', new_column_name='updated_at')

	# ### SurveyFreeformResponse ###
	op.rename_table('freeform_response', 'freeform_responses')
	op.alter_column('freeform_responses', 'date_created', new_column_name='created_at')
	op.alter_column('freeform_responses', 'date_modified', new_column_name='updated_at')

	# ### InteractionLog ###
	op.rename_table('interaction_log', 'interaction_logs')
	op.alter_column('interaction_logs', 'date_created', new_column_name='created_at')

	# ### ContentRating ###
	op.rename_table('content_rating', 'content_ratings')
	op.alter_column('content_ratings', 'date_created', new_column_name='created_at')
	op.alter_column('content_ratings', 'content_id', new_column_name='item_id')
	op.alter_column('content_ratings', 'content_type', new_column_name='item_table_name')
	op.add_column('content_ratings', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

	# ### PreShuffledMovieList ###
	op.add_column('pre_shuffled_movie_lists', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
	op.add_column('pre_shuffled_movie_lists', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

	# ### Demographic ###
	op.alter_column('demographics', 'date_created', new_column_name='created_at')
	op.alter_column('demographics', 'date_updated', new_column_name='updated_at')

	# ### StudyParticipant ###
	op.rename_table('study_participant', 'study_participants')
	op.alter_column('study_participants', 'participant_type', new_column_name='participant_type_id')
	op.alter_column('study_participants', 'current_step', new_column_name='current_step_id')
	op.alter_column('study_participants', 'current_page', new_column_name='current_page_id')
	op.alter_column('study_participants', 'date_created', new_column_name='created_at')
	op.alter_column('study_participants', 'date_updated', new_column_name='updated_at')

	# ### The following tables only need their names changed ###
	op.rename_table('feedback', 'feedbacks')
	op.rename_table('participant_type', 'participant_types')
	op.rename_table('access_log', 'access_logs')


def downgrade() -> None:
	# ### Reversing simple renames ###
	op.rename_table('access_logs', 'access_log')
	op.rename_table('participant_types', 'participant_type')
	op.rename_table('feedbacks', 'feedback')

	# ### StudyParticipant ###
	op.alter_column('study_participants', 'updated_at', new_column_name='date_updated')
	op.alter_column('study_participants', 'created_at', new_column_name='date_created')
	op.alter_column('study_participants', 'current_page_id', new_column_name='current_page')
	op.alter_column('study_participants', 'current_step_id', new_column_name='current_step')
	op.alter_column('study_participants', 'participant_type_id', new_column_name='participant_type')
	op.rename_table('study_participants', 'study_participant')

	# ### Demographic ###
	op.alter_column('demographics', 'updated_at', new_column_name='date_updated')
	op.alter_column('demographics', 'created_at', new_column_name='date_created')

	# ### PreShuffledMovieList ###
	op.drop_column('pre_shuffled_movie_lists', 'updated_at')
	op.drop_column('pre_shuffled_movie_lists', 'deleted_at')

	# ### ContentRating ###
	op.drop_column('content_ratings', 'updated_at')
	op.alter_column('content_ratings', 'item_table_name', new_column_name='content_type')
	op.alter_column('content_ratings', 'item_id', new_column_name='content_id')
	op.alter_column('content_ratings', 'created_at', new_column_name='date_created')
	op.rename_table('content_ratings', 'content_rating')

	# ### InteractionLog ###
	op.alter_column('interaction_logs', 'created_at', new_column_name='date_created')
	op.rename_table('interaction_logs', 'interaction_log')

	# ### SurveyFreeformResponse ###
	op.alter_column('freeform_responses', 'updated_at', new_column_name='date_modified')
	op.alter_column('freeform_responses', 'created_at', new_column_name='date_created')
	op.rename_table('freeform_responses', 'freeform_response')

	# ### SurveyItemResponse ###
	op.alter_column('survey_item_responses', 'scale_level_id', new_column_name='response')
	op.alter_column('survey_item_responses', 'updated_at', new_column_name='date_modified')
	op.alter_column('survey_item_responses', 'created_at', new_column_name='date_created')
	op.rename_table('survey_item_responses', 'survey_item_response')

	# ### PageContents ###
	op.drop_constraint('fk_page_contents_created_by_id_users', 'page_contents', type_='foreignkey')
	op.drop_column('page_contents', 'created_by_id')
	op.drop_column('page_contents', 'updated_at')
	op.drop_column('page_contents', 'deleted_at')
	op.drop_column('page_contents', 'created_at')
	op.alter_column('page_contents', 'construct_id', new_column_name='content_id')
	op.rename_table('page_contents', 'page_content')

	# ### Pages ###
	op.drop_constraint('fk_step_pages_created_by_id_users', 'step_pages', type_='foreignkey')
	op.drop_column('step_pages', 'created_by_id')
	op.drop_column('step_pages', 'updated_at')
	op.drop_column('step_pages', 'deleted_at')
	op.alter_column('step_pages', 'created_at', new_column_name='date_created')
	op.rename_table('step_pages', 'step_page')

	# ### StudySteps ###
	op.drop_constraint('fk_study_steps_created_by_id_users', 'study_steps', type_='foreignkey')
	op.drop_column('study_steps', 'created_by_id')
	op.drop_column('study_steps', 'updated_at')
	op.drop_column('study_steps', 'deleted_at')
	op.alter_column('study_steps', 'created_at', new_column_name='date_created')
	op.rename_table('study_steps', 'study_step')

	# ### StudyConditions ###
	op.drop_constraint('fk_study_conditions_created_by_id_users', 'study_conditions', type_='foreignkey')
	op.drop_column('study_conditions', 'created_by_id')
	op.drop_column('study_conditions', 'updated_at')
	op.drop_column('study_conditions', 'deleted_at')
	op.alter_column('study_conditions', 'created_at', new_column_name='date_created')
	op.rename_table('study_conditions', 'study_condition')

	# ### Studies ###
	op.drop_column('studies', 'updated_at')
	op.drop_column('studies', 'deleted_at')
	op.alter_column('studies', 'created_at', new_column_name='date_created')
	op.rename_table('studies', 'study')

	# ### ScaleLevels ###
	op.drop_constraint('fk_scale_levels_created_by_id_users', 'scale_levels', type_='foreignkey')
	op.drop_column('scale_levels', 'created_by_id')
	op.drop_column('scale_levels', 'updated_at')
	op.drop_column('scale_levels', 'deleted_at')
	op.drop_column('scale_levels', 'created_at')
	op.drop_column('scale_levels', 'notes')
	op.rename_table('scale_levels', 'scale_level')

	# ### ConstructScales ###
	op.drop_constraint('fk_construct_scales_created_by_id_users', 'construct_scales', type_='foreignkey')
	op.drop_column('construct_scales', 'created_by_id')
	op.drop_column('construct_scales', 'updated_at')
	op.drop_column('construct_scales', 'deleted_at')
	op.drop_column('construct_scales', 'created_at')
	op.add_column('construct_scales', sa.Column('created_by', sa.VARCHAR(), autoincrement=False, nullable=True))
	op.rename_table('construct_scales', 'construct_scale')

	# ### SurveyConstructs ###
	op.drop_constraint('fk_survey_constructs_created_by_id_users', 'survey_constructs', type_='foreignkey')
	op.drop_column('survey_constructs', 'created_by_id')
	op.drop_column('survey_constructs', 'updated_at')
	op.drop_column('survey_constructs', 'deleted_at')
	op.drop_column('survey_constructs', 'created_at')
	op.alter_column('survey_constructs', 'description', new_column_name='desc')
	op.rename_table('survey_constructs', 'survey_construct')

	# ### ConstructItems ###
	op.drop_constraint('fk_construct_items_created_by_id_users', 'construct_items', type_='foreignkey')
	op.drop_column('construct_items', 'created_by_id')
	op.drop_column('construct_items', 'updated_at')
	op.drop_column('construct_items', 'deleted_at')
	op.drop_column('construct_items', 'created_at')
	op.drop_column('construct_items', 'notes')
	op.rename_table('construct_items', 'construct_item')

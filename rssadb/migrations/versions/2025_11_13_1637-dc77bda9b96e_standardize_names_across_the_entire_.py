"""Standardize names across the entire database.

This migration standardizes the naming conventions for table names, primary keys,
unique constraints, foreign key constraints, and the corresponding column names
across the entire database schema to ensure consistency and clarity.

Step order:
1. Drop existing foreign key constraints for all tables involved.
2. Rename the specified columns in each table to follow the standardized naming convention.
3. Rename the specified tables to their standardized names.
4. Drop and re-create primary keys and unique constraints with standardized names.
5. Re-create foreign key constraints with standardized names.

Revision ID: dc77bda9b96e
Revises: 173182845d5d
Create Date: 2025-11-13 16:37:38.144644

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = 'dc77bda9b96e'
down_revision: Union[str, None] = '173182845d5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# All foreign key constraints to be renamed
# We will drop these constraints first, then re-create them with standardized names.
# Before we can recreate them, we also have to finish renaming the relevant columns and tables.
FK_TO_DROP: dict[str, list[tuple[str, str, str, str]]] = {
    # table_name: [...(fk_name, local_col, remote_table, remote_col)]
    'api_keys': [
        ('api_keys_study_id_fkey', 'study_id', 'studies', 'id'),
        ('api_keys_user_id_fkey', 'user_id', 'users', 'id'),
    ],
    'construct_items': [
        ('fk_construct_item_survey_construct_id', 'construct_id', 'survey_constructs', 'id'),
        ('fk_construct_items_created_by_id_users', 'created_by_id', 'users', 'id'),
    ],
    'construct_scales': [('fk_construct_scales_created_by_id_users', 'created_by_id', 'users', 'id')],
    'demographics': [('fk_demographics_study_id', 'study_id', 'studies', 'id')],
    'feedbacks': [
        ('feedbacks_step_id_fkey', 'step_id', 'study_steps', 'id'),
        ('feedbacks_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
        ('fk_feedback_study_id', 'study_id', 'studies', 'id'),
        ('fk_feedback_study_participant_id', 'participant_id', 'study_participants', 'id'),
    ],
    'freeform_responses': [
        ('freeform_responses_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
        ('fk_freeform_response_study_participant_id', 'participant_id', 'study_participants', 'id'),
        ('fk_freeform_response_study_step_id', 'step_id', 'study_steps', 'id'),
        ('fk_freeform_response_study_study_id', 'study_id', 'studies', 'id'),
        ('fk_freeform_response_construct_item_id', 'item_id', 'construct_items', 'id'),
        ('freeform_response_item_id_fkey', 'item_id', 'construct_items', 'id'),
    ],
    'page_contents': [
        ('fk_page_content_survey_construct_id', 'construct_id', 'survey_constructs', 'id'),
        ('fk_page_content_scale_id', 'scale_id', 'survey_scales', 'id'),
        ('fk_page_contents_created_by_id_users', 'created_by_id', 'users', 'id'),
        ('fk_page_content_step_page_id', 'page_id', 'step_pages', 'id'),
    ],
    'participant_interaction_logs': [
        ('fk_interaction_log_study_participant_id', 'participant_id', 'study_participants', 'id'),
        ('participant_interaction_logs_step_id_fkey', 'step_id', 'study_steps', 'id'),
        ('participant_interaction_logs_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
        ('participant_interaction_logs_study_id_fkey', 'study_id', 'studies', 'id'),
    ],
    'participant_movie_sessions': [
        ('fk_participant_movie_sessions_participant_id', 'participant_id', 'study_participants', 'id')
    ],
    'participant_ratings': [
        ('participant_ratings_step_id_fkey', 'step_id', 'study_steps', 'id'),
        ('participant_ratings_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
        ('participant_ratings_study_id_fkey', 'study_id', 'studies', 'id'),
        ('fk_content_rating_study_participant_id', 'participant_id', 'study_participants', 'id'),
    ],
    'participant_recommendation_context': [
        ('participant_recommendation_context_participant_id_fkey', 'participant_id', 'study_participants', 'id'),
        ('participant_recommendation_context_step_id_fkey', 'step_id', 'study_steps', 'id'),
        ('participant_recommendation_context_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
        ('participant_recommendation_context_study_id_fkey', 'study_id', 'studies', 'id'),
    ],
    'participant_sessions': [
        ('participant_sessions_participant_id_fkey', 'participant_id', 'study_participants', 'id')
    ],
    'permissions': [('fk_permissions_study_id', 'study_id', 'studies', 'id')],
    'scale_levels': [
        ('fk_scale_level_construct_scale_id', 'scale_id', 'construct_scales', 'id'),
        ('fk_scale_levels_created_by_id_users', 'created_by_id', 'users', 'id'),
    ],
    'step_pages': [
        ('fk_step_page_study_id', 'study_id', 'studies', 'id'),
        ('fk_step_page_study_step_id', 'step_id', 'study_steps', 'id'),
        ('fk_step_pages_created_by_id_users', 'created_by_id', 'users', 'id'),
    ],
    'studies': [
        ('fk_study_created_by_id_users', 'created_by_id', 'users', 'id'),
        ('fk_study_owner_id_users', 'owner_id', 'users', 'id'),
    ],
    'study_conditions': [
        ('fk_study_condition_study_id', 'study_id', 'studies', 'id'),
        ('fk_study_conditions_created_by_id_users', 'created_by_id', 'users', 'id'),
    ],
    'study_interaction_responses': [
        ('study_interaction_responses_participant_id_fkey', 'participant_id', 'study_participants', 'id'),
        ('study_interaction_responses_step_id_fkey', 'step_id', 'study_steps', 'id'),
        ('study_interaction_responses_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
        ('study_interaction_responses_study_id_fkey', 'study_id', 'studies', 'id'),
    ],
    'study_participants': [
        ('fk_study_participant_participant_type_id', 'participant_type_id', 'participant_types', 'id'),
        ('fk_study_participant_step_page_id', 'current_step', 'step_pages', 'id'),
        ('fk_study_participant_study_condition_id', 'condition_id', 'study_conditions', 'id'),
        ('fk_study_participant_study_id', 'study_id', 'studies', 'id'),
        ('fk_study_participant_study_step_current_step', 'current_step', 'study_steps', 'id'),
    ],
    'study_steps': [
        ('fk_study_step_study_id', 'study_id', 'studies', 'id'),
        ('fk_study_steps_created_by_id_users', 'created_by_id', 'users', 'id'),
    ],
    'survey_constructs': [('fk_survey_constructs_created_by_id_users', 'created_by_id', 'users', 'id')],
    'survey_item_responses': [
        ('fk_survey_item_response_construct_item_id', 'item_id', 'construct_items', 'id'),
        ('fk_survey_item_response_construct_scale_id', 'scale_id', 'construct_scales', 'id'),
        ('fk_survey_item_response_scale_level_id', 'scale_level_id', 'construct_scales', 'id'),
        ('fk_survey_item_response_study_participant_id', 'participant_id', 'study_participants', 'id'),
        ('fk_survey_item_response_study_step_id', 'step_id', 'study_steps', 'id'),
        ('fk_survey_item_response_study_study_id', 'study_id', 'studies', 'id'),
        ('fk_survey_item_response_survey_construct_id', 'construct_id', 'survey_constructs', 'id'),
        ('survey_item_responses_step_page_id_fkey', 'step_page_id', 'step_pages', 'id'),
    ],
}

# Mapping of tables and their current primary key names if they differ from the standard convention
# Note: We do not include the new PK names here, as they will be generated using convention 'pk_<table_name>'
PK_RENAME_MAP: dict[str, str] = {
    # table_name: old_pk_name
    'access_logs': 'access_log_pkey',
    'api_keys': 'api_keys_pkey',
    'construct_items': 'construct_item_pkey',
    'construct_scales': 'construct_scale_pkey',
    'demographics': 'demographics_pkey',
    'feedbacks': 'feedback_pkey',
    'freeform_responses': 'freeform_response_pkey',
    'page_contents': '',  # Note: We will create a new PK name in this migration
    'participant_interaction_logs': 'participant_interaction_log_pkey',
    'participant_movie_sessions': 'pk_participant_movie_sessions',
    'participant_ratings': 'content_ratings_pkey',
    'participant_recommendation_context': 'participant_recommendation_context_pkey',
    'participant_sessions': 'participant_sessions_pkey',
    'participant_types': 'participant_type_pkey',
    'permissions': 'permissions_pkey',
    'scale_levels': 'scale_level_pkey',
    'step_pages': 'step_page_pkey',
    'studies': 'study_pkey',
    'study_conditions': 'study_condition_pkey',
    'study_interaction_responses': 'study_interaction_responses_pkey',
    'study_participants': 'study_participant_pkey',
    'study_steps': 'study_step_pkey',
    'survey_constructs': 'survey_constructs_pkey',
    'survey_item_responses': '',  # Note: We will create a new PK name in this migration
    'users': 'users_pkey',
}

UQ_RENAME_MAP: dict[str, list[tuple[str, list[str]]]] = {
    # table_name: [...(old_uq_name, [...columns])]
    # 'feedbacks': [('uq_feedbacks_context', [])],  # Note: we will likely remove the feedbacks table
    'freeform_responses': [('uq_freeform_context', ['study_id', 'study_participant_id', 'context_tag'])],
    'participant_interaction_logs': [
        ('uq_interaction_context_tag', ['study_id', 'study_participant_id', 'context_tag'])
    ],
    'participant_ratings': [('uq_participant_ratings_item', ['study_id', 'study_participant_id', 'item_id'])],
    'participant_recommendation_context': [
        ('uq_study_participant_rec_context', ['study_id', 'study_participant_id', 'context_tag'])
    ],
    'participant_sessions': [('participant_sessions_resume_code_key', ['resume_code'])],
    'permissions': [('uq_permission_name_study_id', ['permission_name', 'study_id'])],
    'study_interaction_responses': [
        ('uq_study_participant_context_tag', ['study_id', 'study_participant_id', 'context_tag'])
    ],
    'study_steps': [('uq_study_step_study_id_path', ['study_id', 'path'])],
    'survey_item_responses': [('uq_survey_item', ['study_id', 'study_participant_id', 'survey_item_id'])],
}

# Mapping of old column names to new standardized column names
# All the changes refer to foreign key columns to address the standardized table names
COL_RENAME_MAP: dict[str, list[tuple[str, str]]] = {
    # table_name: [...(old_col_name, new_col_name)]
    'construct_items': [('construct_id', 'survey_construct_id')],
    'demographics': [('participant_id', 'study_participant_id')],
    'feedbacks': [
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('step_page_id', 'study_step_page_id'),
    ],
    'freeform_responses': [
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('step_page_id', 'study_step_page_id'),
        # Note: we are not renaming the `item_id` column here, instead we will drop it.
    ],
    'page_contents': [
        ('page_id', 'study_step_page_id'),
        ('construct_id', 'survey_construct_id'),
        ('scale_id', 'survey_scale_id'),
    ],
    'participant_interaction_logs': [
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('step_page_id', 'study_step_page_id'),
    ],
    'participant_movie_sessions': [('participant_id', 'study_participant_id')],
    'participant_ratings': [
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('step_page_id', 'study_step_page_id'),
    ],
    'participant_recommendation_context': [
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('step_page_id', 'study_step_page_id'),
    ],
    'participant_sessions': [('participant_id', 'study_participant_id')],
    'scale_levels': [('scale_id', 'survey_scale_id')],
    'step_pages': [('step_id', 'study_step_id')],
    'study_interaction_responses': [
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('step_page_id', 'study_step_page_id'),
    ],
    'study_participants': [
        ('participant_type_id', 'study_participant_type_id'),
        ('condition_id', 'study_condition_id'),
    ],
    'survey_item_responses': [
        ('item_id', 'survey_item_id'),
        ('scale_id', 'survey_scale_id'),
        ('scale_level_id', 'survey_scale_level_id'),
        ('participant_id', 'study_participant_id'),
        ('step_id', 'study_step_id'),
        ('construct_id', 'survey_construct_id'),
        ('step_page_id', 'study_step_page_id'),
    ],
}

# Mapping of old table names to new standardized table names
# Name convention: study_<component>, participant_<component>, survey_<component>
# study_participant_<component> refers to components that are generated by the study for participants
# participant_<interaction/response> refers to a response or action that is created by/for a participant at runtime
TABLE_RENAME_MAP: dict[str, str] = {
    'step_pages': 'study_step_pages',
    'participant_types': 'study_participant_types',
    'page_contents': 'study_step_page_contents',
    'construct_items': 'survey_items',
    'construct_scales': 'survey_scales',
    'scale_levels': 'survey_scale_levels',
    'survey_item_responses': 'participant_survey_responses',
    'study_interaction_responses': 'participant_study_interaction_responses',
    'participant_sessions': 'participant_study_sessions',
    'participant_recommendation_context': 'participant_recommendation_contexts',
    'freeform_responses': 'participant_freeform_responses',
    'demographics': 'participant_demographics',
    'participant_movie_sessions': 'study_participant_movie_sessions',
}

FK_NAMING_MAP: dict[str, list[tuple[str, str, str, Union[str, None]]]] = {
    # table_name: [...(referent_table, local_col, remote_col, ondelete (optional); default CASCADE)]
    # Note: all foreign keys will be created with ondelete='CASCADE' except for those that relates to participants.
    # All participant related FKs will not specify ondelete behavior to avoid accidental deletions.
    'api_keys': [
        ('studies', 'study_id', 'id', 'CASCADE'),
        ('users', 'user_id', 'id', 'CASCADE'),
    ],
    'construct_items': [
        ('survey_constructs', 'survey_construct_id', 'id', 'CASCADE'),
        ('users', 'created_by_id', 'id', 'SET NULL'),
    ],
    'construct_scales': [
        ('users', 'created_by_id', 'id', 'SET NULL'),
    ],
    'demographics': [('study_participants', 'study_participant_id', 'id', 'CASCADE')],
    'feedbacks': [
        ('study_steps', 'study_step_id', 'id', 'CASCADE'),
        ('study_step_pages', 'study_step_page_id', 'id', 'CASCADE'),
        ('studies', 'study_id', 'id', 'CASCADE'),
        ('study_participants', 'study_participant_id', 'id', 'CASCADE'),
    ],
    'freeform_responses': [
        ('study_step_pages', 'study_step_page_id', 'id', None),
        ('study_participants', 'study_participant_id', 'id', None),
        ('study_steps', 'study_step_id', 'id', None),
        ('studies', 'study_id', 'id', None),
        # ('survey_items', 'survey_item_id', 'id', None),
    ],
    'page_contents': [
        ('survey_constructs', 'survey_construct_id', 'id', 'CASCADE'),
        ('survey_scales', 'survey_scale_id', 'id', 'CASCADE'),
        ('users', 'created_by_id', 'id', 'SET NULL'),
        ('study_step_pages', 'study_step_page_id', 'id', 'CASCADE'),
    ],
    'participant_interaction_logs': [
        ('study_participants', 'study_participant_id', 'id', None),
        ('study_steps', 'study_step_id', 'id', None),
        ('study_step_pages', 'study_step_page_id', 'id', None),
        ('studies', 'study_id', 'id', None),
    ],
    'participant_movie_sessions': [
        ('study_participants', 'study_participant_id', 'id', None),
        (
            'pre_shuffled_movie_lists',
            'assigned_list_id',
            'id',
            'CASCADE',
        ),
    ],
    'participant_ratings': [
        ('study_steps', 'study_step_id', 'id', None),
        ('study_step_pages', 'study_step_page_id', 'id', None),
        ('studies', 'study_id', 'id', None),
        ('study_participants', 'study_participant_id', 'id', None),
    ],
    'participant_recommendation_context': [
        ('study_participants', 'study_participant_id', 'id', None),
        ('study_steps', 'study_step_id', 'id', None),
        ('study_step_pages', 'study_step_page_id', 'id', None),
        ('studies', 'study_id', 'id', None),
    ],
    'participant_sessions': [('study_participants', 'study_participant_id', 'id', 'CASCADE')],
    'scale_levels': [
        ('survey_scales', 'survey_scale_id', 'id', 'CASCADE'),
        ('users', 'created_by_id', 'id', 'SET NULL'),
    ],
    'step_pages': [
        ('studies', 'study_id', 'id', 'CASCADE'),
        ('study_steps', 'study_step_id', 'id', 'CASCADE'),
        ('users', 'created_by_id', 'id', 'SET NULL'),
    ],
    'studies': [
        ('users', 'created_by_id', 'id', 'SET NULL'),
        ('users', 'owner_id', 'id', 'SET NULL'),
    ],
    'study_conditions': [
        ('studies', 'study_id', 'id', 'CASCADE'),
        ('users', 'created_by_id', 'id', 'SET NULL'),
    ],
    'study_interaction_responses': [
        ('study_participants', 'study_participant_id', 'id', 'CASCADE'),
        ('study_steps', 'study_step_id', 'id', 'CASCADE'),
        ('study_step_pages', 'study_step_page_id', 'id', 'CASCADE'),
        ('studies', 'study_id', 'id', 'CASCADE'),
    ],
    'study_participants': [
        ('study_participant_types', 'study_participant_type_id', 'id', None),
        ('study_conditions', 'study_condition_id', 'id', None),
        ('studies', 'study_id', 'id', None),
        ('study_steps', 'current_step_id', 'id', None),
        ('study_step_pages', 'current_page_id', 'id', None),
    ],
    'study_steps': [
        ('studies', 'study_id', 'id', 'CASCADE'),
        ('users', 'created_by_id', 'id', 'SET NULL'),
    ],
    'survey_constructs': [('users', 'created_by_id', 'id', 'SET NULL')],
    'survey_item_responses': [
        ('survey_items', 'survey_item_id', 'id', None),
        ('survey_scales', 'survey_scale_id', 'id', None),
        ('survey_scale_levels', 'survey_scale_level_id', 'id', None),
        ('study_participants', 'study_participant_id', 'id', None),
        ('study_steps', 'study_step_id', 'id', None),
        ('studies', 'study_id', 'id', None),
        ('survey_constructs', 'survey_construct_id', 'id', None),
        ('study_step_pages', 'study_step_page_id', 'id', None),
    ],
}

# Naming conventions that will be used for this migration
PK_NAMING_CONVENTION = 'pk_{table_name}'
UQ_NAMING_CONVENTION = 'uq_{table_name}'
FK_NAMING_CONVENTION = 'fk_{table_name}_{local_col}'


def drop_all_foreign_keys() -> None:
    for table_name, fk_names in FK_TO_DROP.items():
        for fk_name in fk_names:
            op.drop_constraint(fk_name[0], table_name, type_='foreignkey')


def rename_all_tables_and_columns() -> None:
    # Second step: Rename columns
    for table_name, col_renames in COL_RENAME_MAP.items():
        for old_col, new_col in col_renames:
            op.alter_column(table_name, old_col, new_column_name=new_col)

    # Third step: Rename tables
    for old_table, new_table in TABLE_RENAME_MAP.items():
        op.rename_table(old_table, new_table)


def drop_create_pk_uq_constraints():
    for table_name, old_pk_name in PK_RENAME_MAP.items():
        actual_table_name = TABLE_RENAME_MAP.get(table_name, table_name)
        if old_pk_name:
            op.drop_constraint(old_pk_name, actual_table_name, type_='primary')
        new_pk_name = PK_NAMING_CONVENTION.format(table_name=actual_table_name)
        op.create_primary_key(new_pk_name, actual_table_name, ['id'])

    for table_name, uq_list in UQ_RENAME_MAP.items():
        actual_table_name = TABLE_RENAME_MAP.get(table_name, table_name)
        for old_uq_name, columns in uq_list:
            op.drop_constraint(old_uq_name, actual_table_name, type_='unique')
            column_names = '_'.join(columns)
            new_uq_name = UQ_NAMING_CONVENTION.format(table_name=actual_table_name, column_names=column_names)
            op.create_unique_constraint(new_uq_name, actual_table_name, columns)


def create_foreign_keys() -> None:
    for table_name, fk_list in FK_NAMING_MAP.items():
        actual_table_name = TABLE_RENAME_MAP.get(table_name, table_name)
        for fk in fk_list:
            referent_table, local_col, remote_col, ondelete = fk

            referent_table_actual = TABLE_RENAME_MAP.get(referent_table, referent_table)
            fk_name = FK_NAMING_CONVENTION.format(table_name=actual_table_name, local_col=local_col)

            op.create_foreign_key(
                fk_name,
                actual_table_name,
                referent_table_actual,
                [local_col],
                [remote_col],
                ondelete=ondelete,
            )


def upgrade() -> None:
    # First step: Drop all foreign key constraints
    drop_all_foreign_keys()

    # Second and third steps: Rename columns and tables
    rename_all_tables_and_columns()

    # Fourth step: Drop and re-create primary keys and unique constraints with standardized names
    drop_create_pk_uq_constraints()

    conn = op.get_bind()
    find_distinct_troubled_ids_query = text("""
        SELECT DISTINCT study_step_id
        FROM (
            SELECT study_step_id
            FROM study_step_pages
            GROUP BY study_step_id, order_position
            HAVING COUNT(*) > 1
        ) AS duplicates;
    """)

    query_result = conn.execute(find_distinct_troubled_ids_query).fetchall()
    troubled_ids = [row[0] for row in query_result]

    if troubled_ids:
        print(f'Found {len(troubled_ids)} study_step_id(s) with duplicate order_position values.')

        for study_step_id in troubled_ids:
            fetch_duplicates_query = text("""
                SELECT id, order_position, created_at
                FROM study_step_pages
                WHERE study_step_id = :step_id_to_fix
                ORDER BY order_position, created_at;
            """)
            pages_to_fix = conn.execute(fetch_duplicates_query, {'step_id_to_fix': study_step_id}).fetchall()

            for index, page_row in enumerate(pages_to_fix):
                new_order_position = index + 1
                page_id = page_row[0]
                update_position_query = text("""
                    UPDATE study_step_pages
                    SET order_position = :new_order_position
                    WHERE id = :page_id;
                """)
                conn.execute(update_position_query, {'new_order_position': new_order_position, 'page_id': page_id})
        print('Duplicate order_position values have been resolved.')
    else:
        print('No duplicate order_position values found.')

    with op.batch_alter_table('study_step_pages') as batch_op:
        batch_op.drop_index('ix_step_page_study_step_page_order')
        batch_op.create_unique_constraint('uq_study_step_pages', ['study_step_id', 'order_position'])

    op.drop_column('participant_freeform_responses', 'item_id')
    # Fifth step: Re-create foreign key constraints with standardized names
    create_foreign_keys()

    # We will manually drop the feedbacks table's unique constraint
    op.drop_constraint('uq_feedbacks_context', 'feedbacks', type_='unique')


def drop_new_foreign_keys() -> None:
    for table_name, fk_list in FK_NAMING_MAP.items():
        actual_table_name = TABLE_RENAME_MAP.get(table_name, table_name)
        for fk in fk_list:
            local_col = fk[1]
            fk_name = FK_NAMING_CONVENTION.format(table_name=actual_table_name, local_col=local_col)
            op.drop_constraint(fk_name, actual_table_name, type_='foreignkey')


def reverse_table_and_column_renames() -> None:
    # Reverse table renames
    for old_table, new_table in TABLE_RENAME_MAP.items():
        op.rename_table(new_table, old_table)

    # Reverse column renames
    for table_name, col_renames in COL_RENAME_MAP.items():
        for old_col, new_col in col_renames:
            op.alter_column(table_name, new_col, new_column_name=old_col)


def drop_create_original_pk_uq_constraints() -> None:
    for table_name, old_pk_name in PK_RENAME_MAP.items():
        actual_table_name = table_name  # since we have reverted the table names
        new_pk_name = PK_NAMING_CONVENTION.format(table_name=actual_table_name)
        op.drop_constraint(new_pk_name, actual_table_name, type_='primary')
        if old_pk_name:
            op.create_primary_key(old_pk_name, actual_table_name, ['id'])

    for table_name, uq_list in UQ_RENAME_MAP.items():
        actual_table_name = table_name  # since we have reverted the table names
        for old_uq_name, columns in uq_list:
            column_names = '_'.join(columns)
            new_uq_name = UQ_NAMING_CONVENTION.format(table_name=actual_table_name, column_names=column_names)
            op.drop_constraint(new_uq_name, actual_table_name, type_='unique')
            op.create_unique_constraint(old_uq_name, actual_table_name, columns)


def recreate_original_foreign_keys() -> None:
    for table_name, fk_names in FK_TO_DROP.items():
        for fk in fk_names:
            fk_name, local_col, remote_table, remote_col = fk
            op.create_foreign_key(fk_name, table_name, remote_table, [local_col], [remote_col])


def downgrade() -> None:
    op.create_unique_constraint(
        'uq_feedbacks_context', 'feedbacks', ['study_id', 'study_participant_id', 'context_tag']
    )
    # First step: Drop all newly created foreign key constraints
    drop_new_foreign_keys()

    # Second and third steps: Rename tables and columns back to original names
    # Reverse table renames
    reverse_table_and_column_renames()

    # Fourth step: Drop and re-create primary keys and unique constraints with original names
    drop_create_original_pk_uq_constraints()

    # Note: this part only reverts the structure, the data update is not reverted.
    op.add_column('freeform_responses', sa.Column('item_id', UUID(as_uuid=True), nullable=True))
    op.drop_constraint('uq_study_step_pages', 'study_step_pages', type_='unique')
    op.create_index(
        'ix_step_page_study_step_page_order', 'step_pages', ['study_id', 'step_id', 'id', 'order_position'], unique=True
    )

    # Fifth step: Re-create original foreign key constraints
    recreate_original_foreign_keys()

"""Rename participant_response to participant_survey_response

Revision ID: b751505559a7
Revises: ca9f562ddf68
Create Date: 2025-03-27 17:40:06.928837

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b751505559a7'
down_revision: Union[str, None] = 'ca9f562ddf68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


old_table_name: str = 'participant_response'
new_table_name: str = 'participant_survey_response'

old_fk_entity_study_participant_id: str = 'fk_participant_response_study_participant_id'
old_fk_entity_survey_construct_id: str = 'fk_participant_response_survey_construct_id'
old_fk_entity_construct_item_id: str = 'fk_participant_response_construct_item_id'

new_fk_entity_study_participant_id: str = 'fk_participant_survey_response_study_participant_id'
new_fk_entity_survey_construct_id: str = 'fk_participant_survey_response_survey_construct_id'
new_fk_entity_construct_item_id: str = 'fk_participant_survey_response_construct_item_id'


def upgrade() -> None:

    # Must drop the foreign keys before renaming the table
    op.drop_constraint(old_fk_entity_study_participant_id, old_table_name, type_='foreignkey')
    op.drop_constraint(old_fk_entity_survey_construct_id, old_table_name, type_='foreignkey')
    op.drop_constraint(old_fk_entity_construct_item_id, old_table_name, type_='foreignkey')
    
    # Must rename the table before creating the new foreign keys
    op.rename_table(old_table_name, new_table_name)

    # foreign key with study_participant
    op.create_foreign_key(
        new_fk_entity_study_participant_id,
        new_table_name,
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # foreign key with survey_construct
    op.create_foreign_key(
        new_fk_entity_survey_construct_id,
        new_table_name,
        'survey_construct',
        ['construct_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # foreign key with construct_item
    op.create_foreign_key(
        new_fk_entity_construct_item_id,
        new_table_name,
        'construct_item',
        ['item_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # Must drop the foreign keys before renaming the table
    op.drop_constraint(new_fk_entity_study_participant_id, new_table_name, type_='foreignkey')
    op.drop_constraint(new_fk_entity_survey_construct_id, new_table_name, type_='foreignkey')
    op.drop_constraint(new_fk_entity_construct_item_id, new_table_name, type_='foreignkey')
    
    # Must rename the table before creating the new foreign keys
    op.rename_table(new_table_name, old_table_name)

    # foreign key with study_participant
    op.create_foreign_key(
        old_fk_entity_study_participant_id,
        old_table_name,
        'study_participant',
        ['participant_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # foreign key with survey_construct
    op.create_foreign_key(
        old_fk_entity_survey_construct_id,
        old_table_name,
        'survey_construct',
        ['construct_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # foreign key with construct_item
    op.create_foreign_key(
        old_fk_entity_construct_item_id,
        old_table_name,
        'construct_item',
        ['item_id'],
        ['id'],
        ondelete='SET NULL'
    )

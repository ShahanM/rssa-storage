"""create tables for construct type and scale definition

Revision ID: 2beaedbc6e85
Revises: 874d09ffbbe1
Create Date: 2024-08-08 20:59:47.644922

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '2beaedbc6e85'
down_revision: Union[str, None] = '874d09ffbbe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		'construct_type',
		sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
		sa.Column('type', sa.String, nullable=False),
		sa.Column('enabled', sa.Boolean, nullable=False),
	)

	op.create_table(
		'construct_scale',
		sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
		sa.Column('levels', sa.Integer, nullable=False),
		sa.Column('name', sa.String, nullable=False),
		sa.Column('enabled', sa.Boolean, nullable=False),
	)

	op.create_table(
		'scale_level',
		sa.Column('level', sa.Integer, nullable=False),
		sa.Column('label', sa.String, nullable=False),
		sa.Column('scale_id', UUID(as_uuid=True), nullable=False),
		sa.Column('enabled', sa.Boolean, nullable=False),
		sa.ForeignKeyConstraint(['scale_id'], ['construct_scale.id'], ondelete='CASCADE'),
	)

	op.add_column('survey_construct', sa.Column('type', UUID(as_uuid=True), nullable=True))

	op.create_foreign_key('fk_survey_construct_type', 'survey_construct', 'construct_type', ['type'], ['id'])

	op.add_column('survey_construct', sa.Column('scale', UUID(as_uuid=True), nullable=True))

	op.create_foreign_key('fk_survey_construct_scale', 'survey_construct', 'construct_scale', ['scale'], ['id'])

	op.add_column('construct_item', sa.Column('enabled', sa.Boolean, nullable=False, default=True))


def downgrade() -> None:
	op.drop_constraint('fk_survey_construct_scale', 'survey_construct', type_='foreignkey')
	op.drop_column('survey_construct', 'scale')

	op.drop_constraint('fk_survey_construct_type', 'survey_construct', type_='foreignkey')
	op.drop_column('survey_construct', 'type')

	op.drop_column('construct_item', 'enabled')

	op.drop_table('scale_level')
	op.drop_table('construct_scale')
	op.drop_table('construct_type')

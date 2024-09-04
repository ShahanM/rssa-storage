"""Create initial tables for study

Revision ID: accaafd84165
Revises: 
Create Date: 2024-07-18 02:23:09.355162

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'accaafd84165'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# Create study table
	op.create_table('study',
		sa.Column('id', UUID(as_uuid=True), default=uuid.uuid4),
		sa.Column('name', sa.String, nullable=False),
		sa.Column('date_created', sa.DateTime, nullable=False,
				default=datetime.now(timezone.utc)),
		sa.Column('description', sa.String, nullable=True),
		sa.Column('enabled', sa.Boolean, nullable=False, default=True),
		sa.PrimaryKeyConstraint('id')
	)

	# Create study_condition table
	op.create_table('study_condition',
		sa.Column('id', UUID(as_uuid=True), default=uuid.uuid4),
		sa.Column('study_id', UUID(as_uuid=True), nullable=False),
		sa.Column('name', sa.String, nullable=False),
		sa.Column('date_created', sa.DateTime, nullable=False,
			default=datetime.now(timezone.utc)),
		sa.Column('enabled', sa.Boolean, nullable=False, default=True),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(['study_id'], ['study.id'])
	)
	
	# Create study_step table
	op.create_table('study_step',
		sa.Column('id', UUID(as_uuid=True), default=uuid.uuid4),
		sa.Column('study_id', UUID(as_uuid=True), nullable=False),
		sa.Column('order_position', sa.Integer, nullable=False),
		sa.Column('name', sa.String, nullable=False),
		sa.Column('description', sa.String, nullable=True),
		sa.Column('date_created', sa.DateTime, nullable=False,
			default=sa.func.now()),
		sa.Column('enabled', sa.Boolean, nullable=False, default=True),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(['study_id'], ['study.id'])
	)
	op.create_index('study_step_study_id_order_position_key',
		'study_step', ['study_id', 'order_position'], unique=True)
	
	# Create page table
	op.create_table('step_page',
		sa.Column('id', UUID(as_uuid=True), default=uuid.uuid4),
		sa.Column('study_id', UUID(as_uuid=True), nullable=False),
		sa.Column('step_id', UUID(as_uuid=True), nullable=False),
		sa.Column('order_position', sa.Integer, nullable=False),
		sa.Column('name', sa.String, nullable=False),
		sa.Column('description', sa.String, nullable=True),
		sa.Column('date_created', sa.DateTime, nullable=False,
			default=sa.func.now()),
		sa.Column('enabled', sa.Boolean, nullable=False, default=True),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(['study_id'], ['study.id']),
		sa.ForeignKeyConstraint(['step_id'], ['study_step.id'])
	)
	op.create_index('page_study_id_step_id_order_position_key',
		'step_page', ['study_id', 'step_id', 'order_position'], unique=True)
	

def downgrade() -> None:
	op.drop_table('study_condition')
	op.drop_table('step_page')
	op.drop_table('study_step')
	op.drop_table('study')


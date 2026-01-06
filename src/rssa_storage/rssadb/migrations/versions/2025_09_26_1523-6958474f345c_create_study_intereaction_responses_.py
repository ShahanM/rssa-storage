"""Create study_intereaction_responses table for structure response data

Revision ID: 6958474f345c
Revises: 6994c9640f8b
Create Date: 2025-09-26 15:23:41.273117

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = '6958474f345c'
down_revision: Union[str, None] = '6994c9640f8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		'study_interaction_responses',
		sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
		sa.Column('study_id', UUID(as_uuid=True), sa.ForeignKey('studies.id'), nullable=False),
		sa.Column('participant_id', UUID(as_uuid=True), sa.ForeignKey('study_participants.id'), nullable=False),
		sa.Column(
			'context_tag',
			sa.String(),
			nullable=False,
			comment='A short name identifying the type of interaction (e.g., Final_Choice, Persona_Selection).',
		),
		sa.Column(
			'payload_json',
			JSONB,
			nullable=False,
			comment="""
            Stores the dynamic structured response payload (e.g., chosen item ID, list rankings, predicted scores).
            """,
		),
		sa.Column(
			'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', now())")
		),
		sa.Column(
			'updated_at',
			sa.TIMESTAMP(timezone=True),
			nullable=False,
			server_default=sa.text("TIMEZONE('utc', now())"),
			onupdate=sa.text("TIMEZONE('utc', now())"),
		),
		sa.UniqueConstraint('study_id', 'participant_id', 'context_tag', name='uq_study_participant_context_tag'),
	)

	op.create_table(
		'participant_recommendation_context',
		sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
		sa.Column('study_id', UUID(as_uuid=True), sa.ForeignKey('studies.id'), nullable=False),
		sa.Column('participant_id', UUID(as_uuid=True), sa.ForeignKey('study_participants.id'), nullable=False),
		sa.Column(
			'step_id',
			UUID(as_uuid=True),
			sa.ForeignKey('study_steps.id'),
			nullable=False,
			comment="""
            The specific step where the recommendation list was displayed. In situations where there are no pages.
            """,
		),
		sa.Column(
			'step_page_id',
			UUID(as_uuid=True),
			sa.ForeignKey('step_pages.id'),
			nullable=True,
			comment='The specific page where the recommendation list was displayed.',
		),
		sa.Column(
			'context_tag',
			sa.String(),
			nullable=False,
			comment='A short name to identify the list type (e.g., Initial_List, Final_List_Shown).',
		),
		sa.Column(
			'recommendations_json',
			JSONB,
			nullable=False,
			comment="""
            Stores the full list of generated recommendations, including ranks, IDs, and any predicted metrics.
            """,
		),
		sa.Column(
			'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', now())")
		),
		sa.Column(
			'updated_at',
			sa.TIMESTAMP(timezone=True),
			nullable=False,
			server_default=sa.text("TIMEZONE('utc', now())"),
			onupdate=sa.text("TIMEZONE('utc', now())"),
		),
		sa.Column('discarded', sa.Boolean, nullable=False, default=False),
		sa.UniqueConstraint('study_id', 'participant_id', 'context_tag', name='uq_study_participant_rec_context'),
	)


def downgrade() -> None:
	op.drop_table('participant_recommendation_context')
	op.drop_table('study_interaction_responses')

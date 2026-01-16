"""create tables for attaching constructs to pages

Revision ID: 874d09ffbbe1
Revises: 8b9ff611facb
Create Date: 2024-07-25 01:39:16.268319

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '874d09ffbbe1'
down_revision: str | None = '8b9ff611facb'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'survey_construct',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('desc', sa.String, nullable=False),
    )

    op.create_table(
        'construct_item_type',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('type', sa.String, nullable=False),
    )

    op.create_table(
        'construct_item',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('construct_id', UUID(as_uuid=True), nullable=False),
        sa.Column('text', sa.String, nullable=False),
        sa.Column('order_position', sa.Integer, nullable=False),
        sa.Column('item_type', UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['construct_id'], ['survey_construct.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['item_type'], ['construct_item_type.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'page_content',
        sa.Column('page_id', UUID(as_uuid=True), nullable=False),
        sa.Column('content_id', UUID(as_uuid=True), nullable=False),
        sa.Column('order_position', sa.Integer, nullable=False),
        sa.Column('enabled', sa.Boolean, nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['survey_construct.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['page_id'], ['step_page.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    op.drop_table('construct_item')
    op.drop_table('construct_item_type')
    op.drop_table('page_content')
    op.drop_table('survey_construct')
